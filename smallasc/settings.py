import os

# Django settings for smallasc project.
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DEBUG = True

PAGE_SIZE = 10

ADMINS = (
    ('Steve Cassidy', 'steve.cassidy@mq.edu.au'),
    #('Suren' , 'shopuz@gmail.com'),
)

MANAGERS = ADMINS

ALLOWED_HOSTS = ['bigasc.apps.alveo.edu.au','bigasc.edu.au', 'localhost','127.0.0.1']


EMAIL_SUBJECT_PREFIX = "[austalk] "
SERVER_EMAIL = "django@austalk.edu.au"

DEFAULT_FROM_EMAIL = "steve.cassidy@mq.edu.au"
#DEFAULT_FROM_EMAIL = "suren.shopushrestha@mq.edu.au"

EMAIL_FROM = "no-reply@austalk.edu.au"
EMAIL_HOST = "mail.science.mq.edu.au"
EMAIL_PORT = 25
EMAIL_USERNAME = ""
EMAIL_PASSWORD = ""

#User and Password for staging only
DB_NAME = DB_USER = DB_PASSWORD = 'bigasc'
DB_HOST = DB_PORT = ''
DB_DETAILS = os.environ.get('DATABASE_URL',None)
if DB_DETAILS:
    tmp1, tmp2 = DB_DETAILS.split('/')[2].split('@')
    DB_NAME = DB_DETAILS.split('/')[-1]
    DB_USER,DB_PASSWORD = tmp1.split(':')
    DB_HOST, DB_PORT = tmp2.split(':')
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': DB_NAME,                # Or path to database file if using sqlite3.
        'USER': DB_USER,                # Not used with sqlite3.
        'PASSWORD': DB_PASSWORD,        # Not used with sqlite3.
        'HOST': DB_HOST,                # Set to empty string for localhost. Not used with sqlite3.
        'PORT': DB_PORT,                # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Australia/Sydney'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-au'

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
MEDIA_ROOT = os.environ.get('MEDIA_ROOT',os.path.join(PROJECT_ROOT, 'mediafiles'))

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.environ.get('STATIC_ROOT',os.path.join(PROJECT_ROOT, 'staticfiles'))

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

ATTACHMENT_LOCATION = 'attachments'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    './static',
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'fl61!=#2!s!na9ohc2=ko*8m$+z=irhy#r)j!isz0jo@=^w9)_'

# List of callables that know how to import templates from various sources.


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # insert your TEMPLATE_DIRS here
            # TODO: This needs to change to an absolute path prior to deployment
            "./templates",
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
            'debug': DEBUG,
        },
    },
]

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware'
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'participantportal.modelspackage.auth.CustomAuthBackend',
)

AUTH_PROFILE_MODULE = 'participantportal.UserProfile'

ROOT_URLCONF = 'smallasc.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'smallasc.wsgi.application'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.flatpages',
    
    'tinymce',
    'flatpages_tinymce',
    # Admin site has been enabled for all smallasc apps
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',

    # 3rd party apps
   # 'lettuce.django',
   'bootstrap_pagination',
    'registration',
    #'registration.supplements.default',
    'registration.contrib.notification',

    # Smallasc applications listed
    'baseapp',
    'browse',
    'search',
    'attachments',
    'participantportal',
    'sso',
    'stats',
    'custom_registration',
)

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
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'applogfile': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(os.path.dirname(os.path.realpath(__file__)), 'smallasc.log'),
            'maxBytes': 1024*1024*15, # 15MB
            'backupCount': 10,
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'smallasc': {
            'handlers': ['applogfile',],
            'level': 'DEBUG',
        },
    }
}


# Custom setting for the login url
LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/"

# SPARQL_ENDPOINT
# SPARQL_ENDPOINT = "http://115.146.93.47/openrdf-sesame/repositories/bigasc_prod"
SPARQL_ENDPOINT = "http://115.146.93.47/openrdf-sesame/repositories/bigasc_native"

# SMALLASCDATA_ENDPOINT
SMALLASCDATA_ENDPOINT = "http://data.austalk.edu.au/download/"

# should we print Sparql queries to the log for debugging?
PRINT_SPARQL = False
# when printing queries, do we want to see all the prefix lines?
PRINT_SPARQL_PREFIXES = False

JWT_SECRET = "austalk_secret"


## django-registration related settings
ACCOUNT_ACTIVATION_DAYS = 7

REGISTRATION_SUPPLEMENT_CLASS = "custom_registration.models.RegistrationCustomFields"

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

TINYMCE_DEFAULT_CONFIG = {
    # custom plugins
    'plugins': "table,spellchecker,paste,searchreplace,media,autosave,example,insertdatetime, preview,template",
    # editor theme
    'theme': "advanced",
    "theme_advanced_buttons3_add" : "cite,abbr",
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 10,
    'height': "450px",

    # use absolute urls when inserting links/images
    'relative_urls': False,
}

FLATPAGES_MEDIA_URL = os.path.join(STATIC_URL, 'flatpages_tinymce')

SITE_ID = 1

#Grab OAuth and Config from Env Variables if exists
try:
    import pyalveo
    
    COLLECTION = "austalk"
    API_URL = os.environ['APP_URL']
    OAUTH_CLIENT_ID = os.environ['CLIENT_ID']
    OAUTH_CLIENT_SECRET = os.environ['CLIENT_SECRET']
    OAUTH_REDIRECT_URL = os.environ['REDIRECT_URL']
    
    #So now we need to init a special client for participants when they login
    #This is dodgy af and may allow unauthorised data access. This is only meant 
    #to be temporary until the participant portal has been updated to only display
    #hidden but publicly available details. As it would be public, this client wouldn't
    #be needed.
    
    #An account has been created in the Alveo app for this purpose.
    #name: Participant Portal
    PP_API_KEY = os.environ['PP_API_KEY']
    
    PPCLIENT = pyalveo.Client(api_url=API_URL,api_key=PP_API_KEY,verifySSL=False).to_json()
except:
    pass

# load local settings
# put customized stuff here
try:
    from smallasc.local_settings import *
except ImportError as e:
    pass

