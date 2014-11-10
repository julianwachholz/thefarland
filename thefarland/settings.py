"""
Django settings for project cookeat.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import dj_config_url
from django.core.exceptions import ImproperlyConfigured


BASE_DIR = os.path.dirname(os.path.dirname(__file__))


def get_env_setting(setting, default=None):
    try:
        return os.environ[setting]
    except KeyError:
        pass
    if default is not None:
        return default
    error_msg = 'Set the %s env variable' % setting
    raise ImproperlyConfigured(error_msg)


DEBUG = get_env_setting('DEBUG', False)
TEMPLATE_DEBUG = DEBUG

SECRET_KEY = get_env_setting('SECRET_KEY', 'dummy' if DEBUG else None)

# TODO: add hosts to ALLOWED_HOSTS
ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'formulation',
    'apps.accounts',
)

AUTH_USER_MODEL = 'accounts.User'

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.ERROR: 'alert',
}

ROOT_URLCONF = 'thefarland.urls'

LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'index'

WSGI_APPLICATION = 'thefarland.wsgi.application'


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': dj_config_url.config(),
}

CACHES = {
    'default': dj_config_url.cache_config(),
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'


if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Paris'
USE_I18N = False
USE_L10N = False
USE_TZ = True

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

if not DEBUG:
    TEMPLATE_LOADERS = (
        ('django.template.loaders.cached.Loader', TEMPLATE_LOADERS),
    )

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

if not DEBUG:
    STATIC_ROOT = get_env_setting('STATIC_ROOT')

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'assets'),
)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


# Celery configuration
from kombu import Exchange, Queue
BROKER_URL = get_env_setting('BROKER_URL')
CELERY_RESULT_BACKEND = BROKER_URL
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_TASK_RESULT_EXPIRES = 3600
CELERY_DEFAULT_QUEUE = 'default'
CELERY_QUEUES = [
    Queue('default', Exchange('default'), routing_key='default'),
    Queue('minecraft', Exchange('minecraft'), routing_key='minecraft'),
]
CELERY_ROUTES = {
    'apps.minecraft.tasks.minecraft_cmd': {
        'queue': 'minecraft',
        'routing_key': 'minecraft',
    },
}
