"""
Django settings for AMY project.
"""

import os
import sys

import environ

from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext_lazy as _


ROOT_DIR = environ.Path(__file__) - 2  # (amy/config/settings.py - 2 = amy/)
BASE_DIR = ROOT_DIR()
APPS_DIR = ROOT_DIR.path('amy')

env = environ.Env()

READ_DOT_ENV_FILE = env.bool('AMY_READ_DOT_ENV_FILE', default=False)
if READ_DOT_ENV_FILE:
    # OS environment variables take precedence over variables from .env
    env.read_env(str(ROOT_DIR.path('.env')))

CONTINUOUS_INTEGRATION = env.bool('CONTINUOUS_INTEGRATION', default=False)

# GENERAL
# -----------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool('AMY_DEBUG', True)
# Local time zone. Choices are
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# though not all of them may be available with every OS.
# In Windows, this must be set to your system time zone.
TIME_ZONE = 'UTC'
# https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'en-us'
# https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1
# https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True
# Secret key must be kept secret
DEFAULT_SECRET_KEY = '3l$35+@a%g!(^y^98oi%ei+%+yvtl3y0k^_7-fmx2oj09-ac5@'
SECRET_KEY = env.str('AMY_SECRET_KEY', default=DEFAULT_SECRET_KEY)
if not DEBUG and SECRET_KEY == DEFAULT_SECRET_KEY:
    raise ImproperlyConfigured('You must specify non-default value for '
                               'SECRET_KEY when running with Debug=FALSE.')

SITE_ID = env.int('AMY_SITE_ID', default=1)
ALLOWED_HOSTS = env.list('AMY_ALLOWED_HOSTS',
                         default=['amy.software-carpentry.org'])
if DEBUG:
    ALLOWED_HOSTS.append('127.0.0.1')

# DATABASES
# -----------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': env.db('DATABASE_URL', default='sqlite:///db.sqlite3'),
}
DATABASES['default']['ATOMIC_REQUESTS'] = True
if '--keepdb' in sys.argv:
    # By default, Django uses in-memory sqlite3 database, which is much
    # faster than sqlite3 database in a file. However, we may want to keep
    # database between test launches, so that we avoid the overhead of
    # applying migrations on each test launch.
    DATABASES['default'].update(dict(TEST=dict(NAME='test_db.sqlite3')))

# URLS
# -----------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = 'config.urls'
# https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'config.wsgi.application'

# PyData extension
# -----------------------------------------------------------------------------
ENABLE_PYDATA = env.bool('AMY_ENABLE_PYDATA', False)
if ENABLE_PYDATA:
    PYDATA_USERNAME_SECRET = env.str('AMY_PYDATA_USERNAME', default='')
    PYDATA_PASSWORD_SECRET = env.str('AMY_PYDATA_PASSWORD', default='')
    if not PYDATA_USERNAME_SECRET or not PYDATA_PASSWORD_SECRET:
        raise ImproperlyConfigured(
            "PyData username and password are required when using "
            "AMY_ENABLE_PYDATA=true.")

# ReCaptcha
# -----------------------------------------------------------------------------
RECAPTCHA_PUBLIC_KEY = env.str('AMY_RECAPTCHA_PUBLIC_KEY', default='')
RECAPTCHA_PRIVATE_KEY = env.str('AMY_RECAPTCHA_PRIVATE_KEY', default='')
RECAPTCHA_USE_SSL = True
NOCAPTCHA = True
if DEBUG:
    os.environ['RECAPTCHA_TESTING'] = 'True'
    if not RECAPTCHA_PUBLIC_KEY:
        RECAPTCHA_PUBLIC_KEY = '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI'
    if not RECAPTCHA_PRIVATE_KEY:
        RECAPTCHA_PRIVATE_KEY = '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe'
else:
    # ensure the keys are present on production
    if not RECAPTCHA_PUBLIC_KEY or not RECAPTCHA_PRIVATE_KEY:
        raise ImproperlyConfigured(
            "Both ReCaptcha keys (public and private) must be present.")

# APPS
# -----------------------------------------------------------------------------
DJANGO_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Handy template tags
    'django.contrib.humanize',

    # for TemplatesSetting form template renderer
    # https://docs.djangoproject.com/en/dev/ref/forms/renderers/
    'django.forms',
]
THIRD_PARTY_APPS = [
    'crispy_forms',
    'django_select2',
    'django.contrib.admin',
    'django_countries',
    'django_filters',
    'reversion',
    'reversion_compare',
    'rest_framework',
    'captcha',
    'compressor',
    'social_django',
    'debug_toolbar',
    'django_extensions',
    'anymail',
    'django_comments',  # this used to be in django.contrib
    'markdownx',
]
PYDATA_APP = [
    'amy.pydata.apps.PyDataConfig',
]
LOCAL_APPS = [
    'amy.workshops.apps.WorkshopsConfig',
    'amy.api.apps.ApiConfig',
    'amy.dashboard.apps.DashboardConfig',
    'amy.extforms.apps.ExtformsConfig',
    'amy.extrequests.apps.ExtrequestsConfig',
    'amy.fiscal.apps.FiscalConfig',
    'amy.reports.apps.ReportsConfig',
    'amy.trainings.apps.TrainingsConfig',
    'amy.extcomments.apps.ExtcommentsConfig',
]
# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
if ENABLE_PYDATA:
    INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PYDATA_APP + LOCAL_APPS
else:
    INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# MIGRATIONS
# -----------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#migration-modules
MIGRATION_MODULES = {
    # 'sites': 'amy.contrib.sites.migrations'
}

# AUTHENTICATION
# -----------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#authentication-backends
AUTHENTICATION_BACKENDS = [
    'social_core.backends.github.GithubOAuth2',
    'django.contrib.auth.backends.ModelBackend',
]
SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ['github']
SOCIAL_AUTH_GITHUB_KEY = env.str('AMY_SOCIAL_AUTH_GITHUB_KEY', default='')
SOCIAL_AUTH_GITHUB_SECRET = env.str('AMY_SOCIAL_AUTH_GITHUB_SECRET', default='')
if not DEBUG and not (SOCIAL_AUTH_GITHUB_KEY and SOCIAL_AUTH_GITHUB_SECRET):
    raise ImproperlyConfigured(
        "Logging using github account will *not* work, "
        "because you didn't set AMY_SOCIAL_AUTH_GITHUB_KEY and/or "
        "AMY_SOCIAL_AUTH_GITHUB_SECRET environment variables."
    )
# Github API token (optional). Setting this token reduces limits and quotes
# on Github API.
GITHUB_API_TOKEN = env('AMY_GITHUB_API_TOKEN', default=None)
SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',

    # If we can't find Person associated with given github account, abort.
    'workshops.github_auth.abort_if_no_user_found',

    # The default pipeline includes 'social.pipeline.user.create_user' here,
    # but we don't want to register a new Person when somebody logs in
    # using GitHub account that is not associated with any Person.

    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
)
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-user-model
AUTH_USER_MODEL = 'workshops.Person'
SOCIAL_AUTH_USER_MODEL = 'workshops.Person'
# https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
LOGIN_REDIRECT_URL = 'dispatch'
# https://docs.djangoproject.com/en/dev/ref/settings/#login-url
LOGIN_URL = 'login'

# PASSWORDS
# -----------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = [
    # https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
]
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
VALIDATION = 'django.contrib.auth.password_validation.'
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': VALIDATION + 'UserAttributeSimilarityValidator',
        'OPTIONS': {
            'user_attributes': ('username', 'personal', 'middle', 'family',
                                'email')
        }
    },
    {
        'NAME': VALIDATION + 'MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 10,
        }
    },
    {
        'NAME': VALIDATION + 'CommonPasswordValidator',
    },
    {
        'NAME': VALIDATION + 'NumericPasswordValidator',
    },
]

# CACHE
# -----------------------------------------------------------------------------
# https://docs.djangoproject.com/en/2.2/topics/cache/#database-caching
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cache_default',
    },
    'select2': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cache_select2',
    }
}

# MIDDLEWARE
# -----------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#middleware
MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'reversion.middleware.RevisionMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'workshops.github_auth.GithubAuthMiddleware',
    'workshops.action_required.PrivacyPolicy',
]

# STATIC
# -----------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(ROOT_DIR('staticfiles'))
# https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [
    str(APPS_DIR.path('static')),
    str(ROOT_DIR.path('node_modules')),
]
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
]

# DJANGO-COMPRESSOR
# -----------------------------------------------------------------------------
# https://django-compressor.readthedocs.io/en/stable/settings/
COMPRESS_ENABLED = not CONTINUOUS_INTEGRATION

COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.rCSSMinFilter',
]
COMPRESS_JS_FILTERS = [
    'compressor.filters.jsmin.JSMinFilter',
]

# MEDIA
# -----------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(ROOT_DIR('mediafiles'))
# https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'

# FORM RENDERER
# -----------------------------------------------------------------------------
# https://docs.djangoproject.com/en/2.1/ref/settings/#form-renderer
# and
# https://docs.djangoproject.com/en/1.11/ref/forms/renderers/
FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'

# TEMPLATES
# -----------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
        'DIRS': [
            str(APPS_DIR.path('templates')),
        ],
        'OPTIONS': {
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
            'debug': DEBUG,
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
            # https://docs.djangoproject.com/en/dev/ref/templates/api/#loader-types
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                # AMY version
                'workshops.context_processors.version',
                # GitHub auth
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],

            # Warn viewers of invalid template strings
            'string_if_invalid': 'XXX-unset-variable-XXX',
        },
    },
]
# http://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# FIXTURES
# -----------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#fixture-dirs
FIXTURE_DIRS = (
    str(APPS_DIR.path('fixtures')),
)

# EMAIL
# -----------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = 'anymail.backends.mailgun.EmailBackend'
if DEBUG:
    # outgoing mails will be stored in `django.core.mail.outbox`
    EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# sender for error emails
SERVER_EMAIL = env('AMY_SERVER_EMAIL', default='root@localhost')

# default sender for non-error messages
DEFAULT_FROM_EMAIL = env('AMY_DEFAULT_FROM_EMAIL', default='webmaster@localhost')

# django-anymail configuration for Mailgun
ANYMAIL = {
    'MAILGUN_API_KEY': env('AMY_MAILGUN_API_KEY', default=None),
    'MAILGUN_SENDER_DOMAIN': env('AMY_MAILGUN_SENDER_DOMAIN', default=None),
}
if not DEBUG and (not ANYMAIL['MAILGUN_API_KEY'] or
                  not ANYMAIL['MAILGUN_SENDER_DOMAIN']):
    raise ImproperlyConfigured("Mailgun settings are required when running "
                               "with DEBUG=False.")


# NOTIFICATIONS
# -----------------------------------------------------------------------------
ADMIN_NOTIFICATION_CRITERIA_DEFAULT = 'team@carpentries.org'

# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL.
ADMIN_URL = env('AMY_ADMIN_URL', default='admin/')
# https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [
    ('Sysadmins ML', 'sysadmin@carpentries.org'),
]
# https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

# messages
# -----------------------------------------------------------------------------
from django.contrib.messages import constants as message_constants
MESSAGE_TAGS = {
    message_constants.INFO: 'alert-info',
    message_constants.SUCCESS: 'alert-success',
    message_constants.WARNING: 'alert-warning',
    message_constants.ERROR: 'alert-danger',
}

# django-countries
# -----------------------------------------------------------------------------
# explicitely add European Union as a country
COUNTRIES_OVERRIDE = {
    'EU': _('European Union'),
    'US': _('United States'),
    'W3': _('Online'),
}

# rest-framework
# -----------------------------------------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework_yaml.parsers.YAMLParser',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework_yaml.renderers.YAMLRenderer',
    ),

    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '50/hour',
        'user': '2000/hour'
    },

    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
}

# logging
# -----------------------------------------------------------------------------
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # merge with default configuration
    'formatters': {
        'verbose': {
            'format': '{asctime}::{levelname}::{message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname}::{message}',
            'style': '{',
        },
    },
    'handlers': {
        'null': {
            'class': 'logging.NullHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'email_backend': EMAIL_BACKEND,
            'include_html': True,
        },
        'log_file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            # `str()` prevents some strange bug on Py3.5
            'filename': str(env.path('AMY_SERVER_LOGFILE', default='amy.log')),
        },
    },
    'loggers': {
        # disable "Invalid HTTP_HOST" notifications
        'django.security.DisallowedHost': {
            'handlers': ['null'],
            'propagate': False,
        },
        'amy': {
            'handlers': ['null', ],
            'level': 'WARNING',
        },
        'amy.server_logs': {
            'handlers': ['log_file', ],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

# Debug Toolbar
# -----------------------------------------------------------------------------
DEBUG_TOOLBAR_PATCH_SETTINGS = False
INTERNAL_IPS = ['127.0.0.1', '::1']

# Django-contrib-comments
# -----------------------------------------------------------------------------
# https://django-contrib-comments.readthedocs.io/en/latest/settings.html
COMMENTS_APP = 'extcomments'

# Django-Select2 settings
# -----------------------------------------------------------------------------
# https://django-select2.readthedocs.io/en/latest/django_select2.html
SELECT2_JS = ''  # don't load JS on it's own - we're loading it in `base.html`
SELECT2_CSS = ''  # the same for CSS
SELECT2_I18N = 'select2/js/i18n'
SELECT2_CACHE_BACKEND = 'select2'
