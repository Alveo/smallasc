import os

# Django settings for smallasc project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

PAGE_SIZE = 10

ADMINS = (
    ('Shirren Premaratne', 'shirren.premaratne@gmail.com'),
    ('Tomas Krajca', 't.l.krajca@gmail.com'),
    ('Steve Cassidy', 'steve.cassidy@mq.edu.au'),
)

MANAGERS = ADMINS

EMAIL_SUBJECT_PREFIX = "[austalk] "
SERVER_EMAIL = "django@austalk.edu.au"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',             # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join (os.getcwd (), 'smallascdb'),  # Or path to database file if using sqlite3.
        'USER': '',                                         # Not used with sqlite3.
        'PASSWORD': '',                                     # Not used with sqlite3.
        'HOST': '',                                         # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                                         # Set to empty string for default. Not used with sqlite3.
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
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

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
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
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

TEMPLATE_DIRS = (
    # TODO: This needs to change to an absolute path prior to deployment
    # "./templates"
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.flatpages',
    
    # Admin site has been enabled for all smallasc apps
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',

    # 3rd party apps
    'lettuce.django',
    'bootstrap-pagination',

    # Smallasc applications listed
    'baseapp',
    'browse',
    'search',
    'participantportal',
    'sso',
    
    'debug_toolbar',
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
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
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
SMALLASCDATA_ENDPOINT = "http://data.austalk.edu.au/download/download/"

JWT_SECRET = "austalk_secret"


# load local settings
# put customized stuff here
try:
    from local_settings import *
except ImportError as e:
    pass
