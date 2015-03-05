# Django settings for spawnsong project.
from __future__ import absolute_import
import os,sys
from celery.schedules import crontab

DEBUG = False
TEMPLATE_DEBUG = DEBUG

PATH_TO_HERE = os.getcwd()

ADMINS = (
    ('Thomas Parslow', 'tom@almostobsolete.net'),
)

ALLOWED_HOSTS = ["spawnsong.herokuapp.com", "spawnsong.com"]
if DEBUG:
    ALLOWED_HOSTS.append("localhost")
# To lockdown pages set a password here and enable the middleware below
LOCKDOWN_PASSWORDS = ("demo",)

BASE_URL = "http://spawnsong.com"

MANAGERS = ADMINS


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = 'staticfiles'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = "/static/"

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    "static",
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

PIPELINE_COMPILERS = (
  'pipeline.compilers.less.LessCompiler',
)

PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.jsmin.JSMinCompressor'

PIPELINE_CSS = {
    'styles': {
        'source_filenames': (
          'less/app.less',
          # 'mediaelement/mediaelementplayer.css',
        ),
        'output_filename': 'css/style.css',
    },
}

PIPELINE_JS = {
    'scripts': {
        'source_filenames': (
          'js/vendor/jquery.js',
          'js/vendor/jquery.form.js',
          'js/vendor/underscore.js',
          'js/vendor/instantclick.js',
          'js/vendor/bootstrap.min.js',
          'js/app.js',
          'mediaelement/mediaelement-and-player.js',
          'endless_pagination/js/endless-pagination.js',
        ),
        'output_filename': 'js/compiled/site.js',
    },
}

PIPELINE_MIMETYPES = (
    ('text/coffeescript', '.coffee'),
    ('text/less', '.less'),
    ('text/javascript', '.js'),
    ('text/x-sass', '.sass'),
    ('text/x-scss', '.scss')
    )

STATICFILES_STORAGE = 'pipeline.storage.PipelineStorage'

PIPELINE_ENABLED = True
#PIPELINE_DISABLE_WRAPPER = True

# If we are on heroku we want to re-define the location of the less binary.
HEROKU_LESSC = os.path.join(PATH_TO_HERE, '/app/.heroku/python/bin/lessc')
if os.path.exists(HEROKU_LESSC):
    PIPELINE_LESS_BINARY = HEROKU_LESSC
    

# Make this unique, and don't share it with anybody.
SECRET_KEY = '70aafb9b05c88cdd116adb4779c11849-bb18f1b98a94a805de5ab7d3b79784e6'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    "djangosecure.middleware.SecurityMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line to password protect the whole site
    # 'lockdown.middleware.LockdownMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'pagination.middleware.PaginationMiddleware'
)

ROOT_URLCONF = 'spawnsong.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'sites.spawnsongsite.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'djangosecure',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.comments',
    'django.contrib.humanize',
    'django.contrib.flatpages',
    'endless_pagination',
    'registration',
    'settings_context_processor',
    'social_auth',
    'lockdown',
    'pipeline',
    'storages',
    'south',
    #'gunicorn',
    'crispy_forms',
    'djcelery',
    'sorl.thumbnail',
    'pagination',
    'kombu.transport.django',
    'avatar',
    'django_extensions',
     'raven.contrib.django.raven_compat',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'media',
    'spawnsong',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
    "settings_context_processor.context_processors.settings",
    "spawnsong.context_processors.new_songs_count",
)

TEMPLATE_VISIBLE_SETTINGS = (
    'STRIPE_PUBLIC_KEY',
    'AVATAR_SIZE',
    )

try:
    from memcacheify import memcacheify
except ImportError:
    print "Failed to import memacheify, no cache configuration will be set!"
else:
    CACHES = memcacheify()

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'social_auth.backends.twitter.TwitterBackend',
)

ACCOUNT_ACTIVATION_DAYS = 7

FACEBOOK_APP_ID = 'TODO'
FACEBOOK_API_SECRET = 'TODO'

FACEBOOK_EXTENDED_PERMISSIONS = ['publish_stream']

#LOGIN_URL          = '/login/facebook/'
LOGIN_URL          = '/login/'

LOGIN_REDIRECT_URL = '/'

# If social account is inactive this probably means that the user set/changed
# his email address and should confirm it.
SOCIAL_AUTH_INACTIVE_USER_URL = '/accounts/register/complete/'
# This redirection is set for Twitter users. If more backends added then this
# should be improved to not bother users from another social networks.
SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/profile/'

AVATAR_GRAVATAR_BACKUP = False
AVATAR_DEFAULT_URL = '/images/user.png'
AVATAR_SIZE = 96 # This should match the size in css.


AWS_STORAGE_BUCKET_NAME = "spawnsong"
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_QUERYSTRING_AUTH = False

#STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse' },
    },
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'stream': sys.stdout,
             'formatter': 'standard'
        },
        'stderr': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['stderr'],
            'level': 'ERROR',
            'propagate': True,
        },
        'spawnsong.tasks': {
            'handlers': ['stderr'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': [],
            'propagate': False,
        },
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}

CELERYBEAT_SCHEDULE = {
    'send-artist-sales-emails': {
        'task': 'spawnsong.tasks.send_artist_sales_emails',
        'schedule': crontab(hour=1, minute=0) # Daily at 1am
    },
    'send-user-new-songs-emails': {
        'task': 'spawnsong.tasks.send_new_song_emails_for_user',
        'schedule': crontab(hour=12, minute=0) # Daily at 12pm
    },
}

SONG_PRICE = 123
CURRENCY = "USD"

CRISPY_TEMPLATE_PACK = 'bootstrap3'

CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend'

BROKER_URL = 'django://'

FFMPEG_EXECUTABLE = "/app/.heroku/vendor/ffmpeg/bin/ffmpeg"

EMAIL_BACKEND = 'django_mailgun.MailgunBackend'

FULL_SONG_FILESIZE_LIMIT = 25 * 1024 * 1024

SNIPPET_LENGTH_LIMIT = 42
SNIPPET_LENGTH_MIN = 23

FILE_UPLOAD_TEMP_DIR = "/tmp"

DEFAULT_FROM_EMAIL = "no-reply@spawnsong.com"

SECURE_SSL_REDIRECT = True
# SECURE_HSTS_SECONDS = 60 * 60  # 1 hour
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_FRAME_DENY = True
SECURE_CONTENT_TYPE_NOSNIFF = True
#SECURE_BROWSER_XSS_FILTER = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


AUDIO_PROFILES_DEFAULT = ["128k_mp3", "192k_mp3"]

SNIPPET_AUDIO_PROFILE = "128k_mp3"
FULL_AUDIO_PROFILE = "192k_mp3"

try:
    from .local_settings import *
    print "Imported local_settings.py"
except ImportError:
    # Heroku setup
    
    # If there isn't a local_settings then get settings from the enviroment

    # Get database settings from DATABASE_URL enviroment, this may be overidden in the local settings
    import dj_database_url
    DATABASES = {'default': dj_database_url.config(default='postgres://localhost')}

    AWS_ACCESS_KEY=os.environ.get("AWS_ACCESS_KEY")
    AWS_SECRET_ACCESS_KEY=os.environ.get("AWS_SECRET_ACCESS_KEY")
    
    MAILGUN_ACCESS_KEY = os.environ.get("MAILGUN_ACCESS_KEY")
    MAILGUN_SERVER_NAME = os.environ.get("MAILGUN_SERVER_NAME")
    
    ECHONEST_API_KEY = os.environ.get("ECHONEST_API_KEY")
    
    TWITTER_CONSUMER_KEY         = os.environ.get("TWITTER_CONSUMER_KEY")
    TWITTER_CONSUMER_SECRET      = os.environ.get("TWITTER_CONSUMER_SECRET")

    STRIPE_PUBLIC_KEY = os.environ.get("STRIPE_PUBLIC_KEY")
    STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY")

import stripe
stripe.api_key = STRIPE_SECRET_KEY

AWS_ACCESS_KEY_ID = AWS_ACCESS_KEY

# Down here so that FFMPEG_EXECUTABLE can be replaced in local_settings
AUDIO_PROFILES = {
    "128k_mp3": {
        "extension": "mp3",
        "command": FFMPEG_EXECUTABLE + " -i {input} -acodec libmp3lame -ab 128k {output}"
    },
    "192k_mp3": {
        "extension": "mp3",
        "command": FFMPEG_EXECUTABLE + " -i {input} -acodec libmp3lame -ab 192k {output}"
    }
}

CRISPY_FAIL_SILENTLY = not DEBUG
