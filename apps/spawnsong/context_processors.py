import models

def new_songs_count(request):
    if not request.user.is_authenticated(): return {"new_songs_count": None}
    return {"new_songs_count": models.Order.objects.filter(purchaser=request.user, web_notified=False, delivered=True).count()}
