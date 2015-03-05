{% block subject %}
This gon' be good.
{% endblock %}

{% block body %}
It's your favorite time of day, again.  To the Playlist!

{{ playlist_url }}

Fresh jams, hot off the press:

{% for order in orders %}
"{{ order.song.title }}" by {{ order.song.artist.get_display_name }}
{% endfor %}

Enjoy!

-Spawnsong
{% endblock %}

{% block html %}
<p>It's your favorite time of day, again.  <a href="{{ playlist_url }}">To the Playlist!</a>

<p>Fresh jams, hot off the press:</p>

<p>
{% for order in orders %}
"{{ order.song.title }}" by {{ order.song.artist.get_display_name }} <br>
{% endfor %}
</p>

<p>Enjoy!</p>

<p>-Spawnsong</p>
{% endblock %}
