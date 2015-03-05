from django import template
from django.utils.safestring import escape
from django.utils.html import conditional_escape

register = template.Library()

# @register.simple_tag
# def username(user_or_artist):
#     return mark_safe(u'<a class="username%s" href="%s">%s</a>' % (escape(artist.get_absolute_url()), escape(artist.user.username)))
