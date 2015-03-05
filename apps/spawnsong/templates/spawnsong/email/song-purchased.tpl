{% block subject %}
Your song "{{song.title}}" has been {% if is_preoder %}pre-{% endif %}ordered on Spawnsong.com!
{% endblock %}

{% block body %}
Hello!

Your song "{{ song.title }}" by {{ song.artist.get_display_name }}
has been {% if is_preoder %}pre-{% endif %}ordered by a user on Spawnsong.com!
{% if is_preoder %}
Now all you need to do is complete the song and upload it!
{% else %}
We'll send you the user the full song right away!
{% endif %}
Regards,

The Spawnsong.com Team
{% endblock %}

{% block html %}
<p>
Hello!
</p>

<p>
Your song "{{ song.title }}" by {{ song.artist.get_display_name }}
has been {% if is_preoder %}pre-{% endif %}ordered by a user on Spawnsong.com!
</p>

<p>
{% if is_preoder %}
Now all you need to do is complete the song and upload it!
{% else %}
We'll send you the user the full song right away!
{% endif %}
</p>

<p>
Regards,
</p>

<p>
The Spawnsong.com Team
</p>
{% endblock %}
