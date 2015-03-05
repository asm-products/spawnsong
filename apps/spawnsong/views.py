from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import loader, RequestContext
from django.http import HttpResponseRedirect, HttpResponse, HttpResponsePermanentRedirect
from django.db.models import Count
from django.db import transaction
import models
import forms
import json
from django.db.models import Q
import simplejson
import stripe
import urllib
import logging
from django.conf import settings
from registration.backends.default.views import RegistrationView as DefaultRegistrationView
from mail_templated import EmailMessage
from django.core.exceptions import MultipleObjectsReturned
from PIL import Image, ImageDraw
import random
import math
from media.models import Audio

logger = logging.getLogger(__name__)

class JsonResponse(HttpResponse):
    """
    JSON response
    """
    def __init__(self, content, mimetype='application/json', status=None, content_type=None):
        super(JsonResponse, self).__init__(
            content=json.dumps(content),
            mimetype=mimetype,
            status=status,
            content_type=content_type,
        )

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def frontpage(request):
    snippets = models.Snippet.objects.visible_to(request.user).filter(state="published")

    if request.GET.get("sort",None) == "new":
        snippets = snippets.order_by("-created_at")
    
    if request.is_ajax():
        template = "spawnsong/parts/snippet-list.html"
    else:
        template = "spawnsong/frontpage.html"
    return render_to_response(
        template,
        {
           "snippets": snippets,
           "sort": request.GET.get("sort", None)
        },
        context_instance=RequestContext(request))

def _snippet_details_json(snippet):
    snippet_details = {
        "beats": snippet.beat_locations(),
        "title": snippet.title,
        "price": snippet.price,
        "visualisation_effect": snippet.visualisation_effect,
    };
    # JSON will be inserted into the HTML template, so need the
    # special encode to get rid of "</script>" in strings
    return simplejson.dumps(
        snippet_details,
        cls=simplejson.encoder.JSONEncoderForHTML)
    

def snippet(request, snippet_id, slug=None):
    snippet = get_object_or_404(
        models.Snippet.objects.visible_to(request.user), pk=snippet_id)

    if snippet.slug != slug:
        return HttpResponsePermanentRedirect(snippet.get_absolute_url())
    
    if snippet.state == "processing" or snippet.state == "processing_error":
        return render_to_response(
            "spawnsong/processing_upload.html",
            {
                "snippet": snippet
            },
            context_instance=RequestContext(request))
        
    editable = request.user.is_authenticated() and snippet.song.artist.user == request.user
    # edit mode is for editing the metadata
    edit_mode = editable and ("edit" in request.GET or snippet.state == "ready")
    deleteable = not models.Order.objects.filter(song=snippet.song).exists()
    if edit_mode:
        if request.method == "POST":
            if "delete" in request.POST and deleteable:
                snippet.delete()
                return HttpResponseRedirect("/")
            form = forms.EditSnippetForm(request.POST, request.FILES, instance=snippet)
            if form.is_valid():
                form.save()
                if "publish" in request.POST:
                    snippet.publish()
                return HttpResponseRedirect(snippet.get_absolute_url())
        else:
            form = forms.EditSnippetForm(instance=snippet)
    else:
        form = None
        # Has a comment been posted?
        if request.method == "POST" and request.POST["badger"] == "":
            comment = request.POST["comment"]
            models.Comment.objects.get_or_create(user=request.user, snippet=snippet, content=comment, ip_address=get_client_ip(request))

                                    
    return render_to_response(
        "spawnsong/snippet.html",
        {
            "snippet_details_json": _snippet_details_json(snippet),
            "snippet": snippet,
            "editable": editable,
            "prompt_first_artist_comment": editable and not snippet.comment_set.exists(),
            "deleteable": deleteable,
            "edit_mode": edit_mode,
            "edit_form": form,
            "order_count": snippet.order_count(),
            "paymentsuccess": "paymentsuccess" in request.GET,
            "paymenterror": request.GET.get("paymenterror", None)
        },
        context_instance=RequestContext(request))

@login_required
def upload_full(request, snippet_id, slug=None):
    is_xhr = 'xhr' in request.POST
    snippet = get_object_or_404(
        models.Snippet.objects.visible_to(request.user), pk=snippet_id, song__artist__user=request.user)
    song = snippet.song
    uploaded = snippet.is_complete()
    if request.method == "POST":
        form = forms.UploadCompleteSongForm(request.POST, request.FILES, instance=song)
        if form.is_valid():
            form.save()
            song.queue_delivery()
            uploaded = True
            if is_xhr:
                return JsonResponse({"redirectTo": request.path})
    else:
        form = forms.UploadCompleteSongForm(instance=song)

    html = loader.render_to_string(
        "spawnsong/upload_full.html",
        {
            "uploaded": uploaded,
            "snippet_details_json": _snippet_details_json(snippet),
            "snippet": snippet,
            "form": form
        },
        context_instance=RequestContext(request))
    if is_xhr:
        return JsonResponse({"html": html})
    else:
        return HttpResponse(html)
    

def download_full(request, order_id, email, token):
    order = get_object_or_404(models.Order, pk=order_id, purchaser_email=email, security_token=token)
    # print "Going to get dowload url", order.song.get_download_url()
    return HttpResponseRedirect(order.song.get_download_url())

@login_required
def upload(request):
    # Requests are sometimes the result of a normal form post and
    # sometimes the result of a XHR request
    form = forms.UploadSnippetForm()
    is_xhr = 'xhr' in request.POST
    if request.method == 'POST':
        print (request.POST, request.FILES)
        form = forms.UploadSnippetForm(request.POST, request.FILES)
        if form.is_valid():
            snippet = form.save(request.user)
            if is_xhr:
                return JsonResponse({"redirectTo": snippet.get_absolute_url()})
            else:
                return HttpResponseRedirect(snippet.get_absolute_url())
    else:
        form = forms.UploadSnippetForm()
    html = loader.render_to_string(
        "spawnsong/upload.html",
        {
           "form": form 
        },
        context_instance=RequestContext(request))
    if is_xhr:
        return JsonResponse({"html": html})
    else:
        return HttpResponse(html)

def user(request, username):
    artist = get_object_or_404(models.Artist, user__username=username)
    snippets = models.Snippet.objects.visible_to(request.user).filter(song__artist=artist).select_related('song').filter(Q(state="published") | Q(state="ready"))
    return render_to_response(
        "spawnsong/user.html",
        {
           "artist": artist,
           "user": request.user,
           "snippets": snippets
        },
        context_instance=RequestContext(request))

def search(request):
    query = request.GET.get("q","")
    snippets = models.Snippet.objects \
      .visible_to(request.user) \
      .select_related('song') \
      .filter(Q(state="published") | Q(state="ready")) \
      .filter(Q(title__icontains=query) | Q(song__artist__user__username__icontains=query) | Q(genres__icontains=query))
    return render_to_response(
        "spawnsong/search.html",
        {
           "snippets": snippets
        },
        context_instance=RequestContext(request))

def purchase(request):
    token = request.POST["token"]
    email = request.POST["email"]
    snippet_id = request.POST["snippet_id"]
    snippet = get_object_or_404(models.Snippet, pk=snippet_id)

    if models.Order.objects.filter(purchaser_email=email, song=snippet.song).exists():
        return HttpResponseRedirect(snippet.get_absolute_url() + "?paymenterror=" + urllib.quote("You have already purchased this song!"))
        

    # First authorize the charge on the card with stripe
    try:
        customer = stripe.Customer.create(
            email=email,
            card=token,
            )
    except stripe.CardError, e:
        logger.info("Card declined for %s buying %s" % (email,snippet.id))
        return HttpResponseRedirect(snippet.get_absolute_url() + "?paymenterror=" + urllib.quote("Sorry, your card has been declined"))
    except:
        logger.exception("Failed to process card")
        return HttpResponseRedirect(snippet.get_absolute_url() + "?paymenterror=" + urllib.quote("Sorry, there was an error processing your card"))

    try:
        with transaction.atomic():
            try:
                artistpayment, created =  models.ArtistPayment.objects.select_for_update().get_or_create(
                    artist=snippet.song.artist, paid=False)
            except MultipleObjectsReturned:
                # Because the admin can said paid status it is
                # possible to get multiple paid objects, this needs to
                # be handled
                artistpayment =  models.ArtistPayment.objects.select_for_update().order_by("-created_at").filter(
                    artist=snippet.song.artist, paid=False).first()
                
            
            # Next create the order object in our db
            order = models.Order.objects.create(
                song=snippet.song, 
                artist_payment=artistpayment,
                purchaser=request.user if request.user.is_authenticated() else None,
                purchaser_email=email,
                price=snippet.price,
                stripe_customer_id=customer.id)

            order.maybe_queue_delivery()
    except:
        logger.exception("Failed to capture charge")
        return HttpResponseRedirect(snippet.get_absolute_url() + "?paymenterror=" + urllib.quote("Sorry, there was an error processing your card"))
    
    # Send email to purchaser
    try:
        message = EmailMessage('spawnsong/email/order-song.tpl', {'order': order, 'song': snippet.song, 'is_preorder': not snippet.is_complete()}, to=[order.purchaser_email])
        message.send()
    except:
        logger.exception("Failed to send email receipt")
    
    # # Send email to artist
    # message = EmailMessage('spawnsong/email/song-purchased.tpl', {'order': order, 'song': snippet.song, 'is_preorder': not snippet.is_complete()}, to=[snippet.song.artist.user.email])
    # message.send()

    snippet.update_ordering_score()
    
    return HttpResponseRedirect(snippet.get_absolute_url() + "?paymentsuccess")

class RegistrationView(DefaultRegistrationView):
    pass

@login_required
def personal_playlist(request):
    orders = models.Order.objects.available_or_upcoming(request.user).select_related("song__snippet").order_by("-created_at")
    # Remove the new song count, we've seen them now
    orders.filter(delivered=True).update(web_notified=True)
    songs = [o.song for o in orders]
    if request.is_ajax():
        template = "spawnsong/parts/song-players.html"
    else:
        template = "spawnsong/personal-playlist.html",
    return render_to_response(
        template,
        {
           "songs": songs
        },
        context_instance=RequestContext(request))


def waveform_image(request, width, height, background, foreground, audio_id):
    audio = get_object_or_404(Audio, pk=audio_id)

    segments = audio.echonest_track_analysis["segments"]

    if "," in background:
        background = tuple(map(int, background.split(",")))
    if "," in foreground:
        foreground = tuple(map(int, foreground.split(",")))
    
    width = int(width)
    height = int(height)
    
    im = Image.new("RGB",(width, height), background)
    draw = ImageDraw.Draw(im)
    
    maxvol = max(x["loudness_max"] for x in segments)
    minvol = min(x["loudness_max"] for x in segments)
    length = segments[-1]["start"]

    r = random.Random()
    r.seed(width*height)
    
    for (seg, nextSeg) in zip(segments, segments[1:]):
        t = seg["start"]
        t2 = nextSeg["start"]
        mv = seg["loudness_max"]
        sv = seg["loudness_start"]
        
        start = int(round(t/length * width))
        end = int(round(t2/length * width))
        for p in range(start,end):
            v = (r.random() * (mv-sv)) + sv
            #v = mv
            h = ((v - minvol) / (maxvol-minvol)) * height
            draw.rectangle(((p,height-h),(p,height)), foreground)
            
    response = HttpResponse(mimetype="image/png")
    im.save(response, "PNG")
    response['Cache-Control'] = 'max-age=999999999999'
    return response

@login_required
def edit_user_profile(request):
    if request.method == 'POST':
        form = forms.UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save(request)
            logout(request)
            return HttpResponseRedirect(reverse('registration_complete'))
    else:
        form = forms.UserProfileForm(instance=request.user)
    html = loader.render_to_string(
        "spawnsong/edit_user_profile.html",
        {
            "form": form
        },
        context_instance=RequestContext(request))
    return HttpResponse(html)
