{% block subject %}
Charge failed on Spawnsong
{% endblock %}

{% block body %}
Sorry, but we failed to charge your card for your order of {{ order.song.title }} by {{ order.song.artist.get_display_name }}.

-Spawnsong
{% endblock %}

{% block html %}
<p>Sorry, but we failed to charge your card for your order of {{ order.song.title }} by {{ order.song.artist.get_display_name }}.</p>

<p>-Spawnsong</p>
{% endblock %}
