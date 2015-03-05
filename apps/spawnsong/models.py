# Initial model outline, not tested yet

from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.conf import settings
import datetime
from jsonfield import JSONField
from django.db.models import Q
import uuid
from sorl.thumbnail import ImageField
import storages
from storages.backends import s3boto
import uuid
from django.template.defaultfilters import slugify
import stripe
from media.models import Audio
import celery
from django.template.defaultfilters import slugify

def upload_to(prefix="uploads"):
    def get_file_path(instance, filename):
        ext = filename.split('.')[-1]
        filename = "%s.%s" % (uuid.uuid4(), ext)
        return "%s/%s" % (prefix, filename)
    return get_file_path

class PrivateDownloadStorage(s3boto.S3BotoStorage):
    def __init__(self, *args, **kwargs):
        kwargs.update(dict(
            acl='private',
            querystring_auth=True,
            querystring_expire=600, # 10 minutes, try to ensure people won't/can't share
            ))
        super(PrivateDownloadStorage, self).__init__(*args, **kwargs)
        
    
    def url(self, name, download_file_name=None):
        name = self._normalize_name(self._clean_name(name))
        if self.custom_domain:
            return "%s://%s/%s" % ('https' if self.secure_urls else 'http',
                                   self.custom_domain, name)
        headers = {}
        if download_file_name:
            headers["response-content-disposition"] = "attachment; filename=%s" % (download_file_name,)
        return self.connection.generate_url(self.querystring_expire,
            method='GET', bucket=self.bucket.name, key=self._encode_name(name),
            response_headers=headers,
            query_auth=self.querystring_auth, force_http=not self.secure_urls)

protected_storage = PrivateDownloadStorage()

class Artist(models.Model):
    user = models.OneToOneField(User)

    def get_absolute_url(self):
        return reverse("user", args=(self.user.username,))

    def get_display_name(self):
        return self.user.username

    def __unicode__(self):
        return unicode(self.user)
    
class Song(models.Model):
    """
    A song that a snippet comes from.

    In phase 1 each song has only one snippet, they're split out so we
    can add features later
    """
    artist = models.ForeignKey(Artist)
    
    created_at = models.DateTimeField(default=datetime.datetime.now)
    
    complete_audio = models.ForeignKey(Audio, blank=True, null=True)
    completed_at = models.DateTimeField(null=True, help_text="The time at which the completed audio file was uploaded", blank=True)

    @property
    def complete_audio_mp3(self):
        audioformat =  self.complete_audio.get_format(settings.FULL_AUDIO_PROFILE)
        return audioformat and audioformat.audio_data

    def get_download_url(self):
        "Get a download url for the full audio, the url will expire after 10 minutes. It will also force a download (not play in browser)"
        #print "Get download url"
        return self.complete_audio.original.storage.url(self.complete_audio.original.name, slugify(self.title) + ".mp3")

    def save(self, *args, **kwargs):
        if self.complete_audio and not self.completed_at:
            self.completed_at = datetime.datetime.now()
        return super(Song, self).save(*args, **kwargs)

    def queue_delivery(self):
        import tasks
        if self.is_complete():
            tasks.deliver_full_song.delay(self.id)

    @property
    def title(self):
        snippet = self.snippet_set.first()
        if not snippet: return "<NO TITLE>"
        return snippet.title

    def is_complete(self):
        return self.completed_at is not None

    def __unicode__(self):
        return self.title
        # return u"Song id %d by %s" % (self.id, self.artist)

    def get_absolute_url(self):
        snippet = self.snippet_set.first()
        if not snippet: return None
        return snippet.get_absolute_url()
        

class SnippetManager(models.Manager):
    def visible_to(self, user):
        q = Q(state="published")
        if user and user.is_authenticated():
           q = q | Q(song__artist__user=user)
        return self.filter(q)
    
class Snippet(models.Model):
    """
    A snippet of a song on the site
    """
    song = models.ForeignKey(Song)
    title = models.CharField(max_length=255)
    message = models.CharField(max_length=255, blank=True, help_text='Special message to display above the cover image')
    state = models.CharField(
        max_length=20,
        choices=(
            ("initial"        , "Initial"),
            ("processing"        , "Processing"),
            ("processing_failed" , "Processing Failed"),
            ("ready"             , "Ready"),
            ("published"         , "Published")),
        default="initial")

    created_at = models.DateTimeField(default=datetime.datetime.now)

    image = ImageField(upload_to=upload_to("snippets/images"))

    audio = models.ForeignKey(Audio, null=True)
    
    visualisation_effect = models.CharField(max_length=20, choices=(("pulsate", "Pulsate"), ("none", "None")), default="pulsate")

    ordering_score = models.IntegerField(default=0, help_text="Score used to order snippets on front page, calcualted from number of orders at the moment")

    genres = models.CharField(max_length=255, blank=True)

    processing_error = models.CharField(max_length=255, null=True, help_text="Error message to display to user if we're in processing_error state")
    
    objects = SnippetManager()

    @property
    def slug(self):
        return slugify(self.title)
    
    @property
    def audio_mp3(self):
        audio_format = self.audio.get_format(settings.SNIPPET_AUDIO_PROFILE)
        return audio_format and audio_format.audio_data

    def update_ordering_score(self):
        self.ordering_score = self.song.order_set.count()
        self.save()

    def is_complete(self):
        return self.song.is_complete()

    def order_count(self):
        return self.song.order_set.count()
        
    def comment_count(self):
        return self.comment_set.count()

    def audio_ready(self):
        return bool(self.audio_mp3)

    def beat_locations(self):
        return self.audio and self.audio.echonest_track_analysis and [x["start"] for x in self.audio.echonest_track_analysis["beats"]]

    def maybe_ready(self, commit=True):
        "Move to ready state if the needed info has been retrieved"
        assert self.state == "processing" 
        if self.audio_mp3 and self.audio.echonest_track_analysis:
            self.mark_ready(commit=commit)

    def set_processing_error(self, error="Failed to process audio, it may be in an unsupported format", commit=True):
        assert self.state =="processing"
        self.state = "processing_error"
        self.processing_error = error
        if commit:
            self.save()
    
    def mark_ready(self, commit=True):
       assert self.state == "processing" 
       assert self.audio_mp3, "Audio should be present before the snippet is marked as ready"
       assert self.audio.echonest_track_analysis is not None, "Echonest data should be present before snippet is marked as ready"
       self.state = "ready"
       
       if commit:
           self.save()
           
    def publish(self, commit=True):
       assert self.state == "ready" 
       self.state = "published"
       if commit:
           self.save()

    def process_uploaded_audio(self, commit=True):
        import tasks
        assert self.state in ["processing_error","initial"]
        self.state = "processing"
        
        if commit:
            self.save()
        
        celery.group([
            self.audio.transcode_subtask([settings.SNIPPET_AUDIO_PROFILE]),
            tasks.request_echonest_data_snippet.s(self.id)
            ]).apply_async(
                link=tasks.complete_snippet_processing.si(self.id),
                link_error=tasks.fail_snippet_processing.si(self.id))
        

    @property
    def price(self):
        return settings.SONG_PRICE

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("snippet", args=(self.id, self.slug))
        
    class Meta:
        ordering = ("-ordering_score","-created_at", )
    

class ArtistPayment(models.Model):
    "A payment that the system caluclated is owed to an artist"
    artist = models.ForeignKey(Artist)
    created_at = models.DateTimeField(default=datetime.datetime.now)
    paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.paid and not self.paid_at:
            self.paid_at = datetime.datetime.now()
        return super(ArtistPayment, self).save(*args, **kwargs)

    def __unicode__(self):
        return "Payment to %s" % (self.artist,)


class OrderManager(models.Manager):
    def available_to(self, user):
        "All orders that are delivered and not refunded"
        return self.filter(purchaser=user, delivered=True, refunded=False)
        
    def available_or_upcoming(self, user):
        "All orders that are delivered and not refunded"
        return self.filter(purchaser=user, refunded=False)
        
class Order(models.Model):
    "A pre-order or order for a song"
    artist_payment = models.ForeignKey(ArtistPayment)
    song = models.ForeignKey(Song)
    purchaser = models.ForeignKey(User, null=True, blank=True)
    purchaser_email = models.EmailField()
    price = models.IntegerField(help_text="Purchase price in cents")
    refunded = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)
    
    
    created_at = models.DateTimeField(default=datetime.datetime.now)

    stripe_transaction_id = models.CharField(max_length=255, blank=True)
    stripe_customer_id = models.CharField(max_length=255)
    charged = models.BooleanField(default=False)
    charge_failed = models.BooleanField(default=False)
    charge_error = models.CharField(max_length=255, blank=True)

    security_token = models.CharField(max_length=16, default=lambda : uuid.uuid4().hex[:16])

    web_notified = models.BooleanField(default=False)
    email_notified = models.BooleanField(default=False)

    objects = OrderManager()

    def download_link(self):
        return settings.BASE_URL + reverse("snippet-download-full", args=(self.id, self.purchaser_email, self.security_token))

    def maybe_queue_delivery(self):
        import tasks
        if self.song.is_complete():
            tasks.deliver_full_song_to_order.delay(self.id)

    def refund(self):
        if self.charged:
          ch = stripe.Charge.retrieve(self.stripe_transaction_id)
          if not ch.refunded:
              ch.refund()
        self.refunded = True
        self.save()
            
    def __unicode__(self):
        return "Order for %s by %s" % (self.song, self.purchaser)

class Comment(models.Model):
    """
    A comment on a snippet.
    """
    user = models.ForeignKey(User)
    snippet = models.ForeignKey(Snippet)
    created_at = models.DateTimeField(default=datetime.datetime.now)
    content = models.TextField()
    ip_address = models.GenericIPAddressField(('IP address'), unpack_ipv4=True, blank=True, null=True)

    is_displayed = models.BooleanField(default=True)

    class Meta:
        ordering = ("created_at",)
        unique_together = (("user", "snippet", "content"),)
        
    def __unicode__(self):
        return u"%s: %s" % (self.user, self.content)
    
