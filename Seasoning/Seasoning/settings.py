# Django settings for Seasoning project.
import os
from Seasoning.Seasoning import secrets

# Debug settings
DEBUG = True
TEMPLATE_DEBUG = DEBUG

# The directory containing this file
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# The file to which the database backed up should be written
DB_BACKUP_FILE = os.path.join(BASE_DIR, '../../seasoning_db.bak')

ADMINS = (
    ('Joep Driesen', 'joeper_100@hotmail.com'),
    ('Bram Somers', 'somersbram@gmail.com'),
)

MANAGERS = ADMINS

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': secrets.DATABASE_NAME,                      # Or path to database file if using sqlite3.
        'USER': secrets.DATABASE_USER,                      # Not used with sqlite3.
        'PASSWORD': secrets.DATABASE_PASSWORD,                  # Not used with sqlite3.
        'HOST': secrets.DATABASE_HOST,                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': secrets.DATABASE_PORT,                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Email configuration
EMAIL_HOST = secrets.EMAIL_HOST
EMAIL_PORT = secrets.EMAIL_PORT
EMAIL_HOST_USER = secrets.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = secrets.EMAIL_HOST_PASSWORD
EMAIL_USE_TLS = secrets.EMAIL_USE_TLS
DEFAULT_FROM_EMAIL = 'activation@seasoning.be'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = None

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# During development, 
MEDIA_ROOT = secrets.MEDIA_ROOT
STATIC_ROOT = secrets.STATIC_ROOT

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    BASE_DIR + '/Seasoning/static',
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

# A tuple of callables that are used to populate the context in RequestContext. 
# These callables take a request object as their argument and return a dictionary 
# of items to be merged into the context.
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.core.context_processors.request",
    'django.contrib.messages.context_processors.messages',
)


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'Seasoning.urls'

# Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
# Always use forward slashes, even on Windows.
# Don't forget to use absolute paths, not relative paths.
TEMPLATE_DIRS = (
    BASE_DIR + '/Seasoning/templates',
)

INSTALLED_APPS = (
    'django.contrib.staticfiles',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.humanize',
    'django.contrib.sites',
    'django.contrib.comments',
    'django.contrib.messages',
    
    # Authentication:
    'django.contrib.auth',
    'authentication',
    'captcha',
    
    # Core functionality
    'ingredients',
    'recipes',
)

AUTH_USER_MODEL = 'authentication.User'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
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
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['console']
        }
    }
}

# The URL where requests are redirected for login, especially when using the login_required() decorator.
LOGIN_URL = '/login/'

# The URL where requests are redirected after login when the contrib.auth.login view gets no next parameter.
LOGIN_REDIRECT_URL = '/'

# Used by the authentication. Defines how many days an unactivated accounts will be stored in the database at the least.
ACCOUNT_ACTIVATION_DAYS = 7

# Registration is closed during development
REGISTRATION_OPEN = False

# Django secret key
SECRET_KEY = secrets.SECRET_KEY


# Django-recaptcha
RECAPTCHA_PUBLIC_KEY = '6LcgBtwSAAAAAGYLzvpNQ1tbir0HCabUNV56R1Gk'
RECAPTCHA_PRIVATE_KEY = secrets.RECAPTCHA_PRIVATE_KEY
