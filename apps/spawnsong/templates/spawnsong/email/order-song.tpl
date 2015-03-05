{% block subject %}
Thanks for {% if is_preoder %}pre-{% endif %}ordering "{{ song.title }}" from Spawnsong.com
{% endblock %}

{% block body %}
Hello!

Thanks for ordering "{{ song.title }}" by {{ song.artist.get_display_name }}
on Spawnsong.com!
{% if is_preoder %}
We'll send you the full song once the artist has completed it!
{% else %}
We'll send you the full song right away!
{% endif %}
Regards,

The Spawnsong.com Team
{% endblock %}

{% block html %}
<p>
Hello!
</p>

<p>
Thanks for ordering "{{ song.title }}" by {{ song.artist.get_display_name }}
on Spawnsong.com!
</p>

<p>
{% if is_preoder %}
We'll send you the full song once the artist has completed it!
{% else %}
We'll send you the full song right away!
{% endif %}
</p>

<p>
Regards,
</p>

<p>
The Spawnsong.com Team
</p>
{% endblock %}
