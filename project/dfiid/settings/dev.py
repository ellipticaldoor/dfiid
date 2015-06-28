from dfiid.settings.base import *

DEBUG = True

INSTALLED_APPS += (
	'debug_toolbar',
)

MIDDLEWARE_CLASSES += (
	'debug_toolbar.middleware.DebugToolbarMiddleware',
)

DEBUG_TOOLBAR_CONFIG = {
	'JQUERY_URL': '/s/js/lib/jquery_2.1.3.min.js',
}

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
