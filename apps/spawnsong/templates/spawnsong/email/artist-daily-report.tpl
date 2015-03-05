{% block subject %}
Your Spawnsong.com orders for yesterday
{% endblock %}

{% block body %}
Hello!

Your song(s) recieved orders from users on Spawnsong.com yesterday.

The followin songs received orders:
{% for song in songs %}
"{{ song.title }}" had {{ song.order_count }} {% if not song.is_complete %}pre-{% endif %}orders{% endfor %}

The Spawnsong.com Team
{% endblock %}

{% block html %}
<p>
Hello!
</p>

<p>
Your song(s) recieved orders from users on Spawnsong.com yesterday.
</p>

<p>
The followin songs received orders:
</p>

<p>
{% for song in songs %}
"{{ song.title }}" had {{ song.order_count }} {% if not song.is_complete %}pre-{% endif %}orders<br/>
{% endfor %}
</p>

<p>
Regards,
</p>

<p>
The Spawnsong.com Team
</p>
{% endblock %}
