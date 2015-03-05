{% block subject %}
Full song delivery from Spawnsong.com for "{{ song.title }}"
{% endblock %}

{% block body %}
Hello!

Thanks for ordering "{{ song.title }}" by {{ song.artist.get_display_name }}
on Spawnsong.com! The song is now available for you to download by
clicking on the link below:

{{ order.download_link }}

Please don't share this link, it's just for you!

Regards,

The Spawnsong.com Team
{% endblock %}

{% block html %}
<p>
Hello!
</p>

<p>
Thanks for ordering "{{ song.title }}" by {{ song.artist.get_display_name }}
on Spawnsong.com! The song is now available for you to <a href="{{ order.download_link }}">download by
clicking here.</a>
</p>

<p>
Please don't share this link, it's just for you!
</p>

<p>
Regards,
</p>

<p>
The Spawnsong.com Team
</p>
{% endblock %}
