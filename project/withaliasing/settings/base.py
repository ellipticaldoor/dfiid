"""
Django settings for withaliasing project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


# Normally you should not import ANYTHING from Django directly
# into your settings, but ImproperlyConfigured is an exception.
from django.core.exceptions import ImproperlyConfigured

def get_env(setting):
	""" Get the environment setting or return exception """
	try:
		return os.environ[setting]
	except KeyError:
		error_msg = 'Set the %s env variable' % setting
		raise ImproperlyConfigured(error_msg)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = (
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'markdown_deux',
	'compressor',
	'core',
	'user',
	'blog',
	'cms',
)

MIDDLEWARE_CLASSES = (
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'withaliasing.urls'

WSGI_APPLICATION = 'withaliasing.wsgi.application'

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql_psycopg2',
		'NAME': get_env('DB_NAME'),
		'USER': get_env('DB_USER'),
		'PASSWORD': get_env('DB_PASSWORD'),
		'HOST': get_env('DB_HOST'),
		'PORT': get_env('DB_PORT'),
	}
}

LANGUAGE_CODE = get_env('LANGUAGE')

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/s/'

STATICFILES_DIRS = (
	os.path.join(BASE_DIR, 's'),
)

TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

AUTH_USER_MODEL = 'user.User'

LOGIN_URL = '/login'

COMPRESS_ROOT = os.path.join(BASE_DIR, 's')

COMPRESS_ENABLED = False

COMPRESS_CSS_FILTERS = ['compressor.filters.css_default.CssAbsoluteFilter',  'compressor.filters.cssmin.CSSMinFilter']

STATICFILES_FINDERS = (
	'django.contrib.staticfiles.finders.FileSystemFinder',
	'django.contrib.staticfiles.finders.AppDirectoriesFinder',
	'compressor.finders.CompressorFinder',
)

MARKDOWN_DEUX_STYLES = {
	'default': {
		'safe_mode': False,
	},
}
