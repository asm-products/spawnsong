#web: honcho -f ProcfileHoncho start
web: python manage.py collectstatic --noinput;  python manage.py runserver 0.0.0.0:$PORT
celeryd: python manage.py celeryd
celerybeat: honcho -f ProcfileCelerybeat start
