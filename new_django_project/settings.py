# coding: utf-8

import os

BASE_DIR = os.path.dirname(os.path.join(os.path.dirname(__file__), 'new_django_project'))

DEBUG = False


try:
    from config import *
except ImportError, e:
    pass


ROOT_URLCONF = 'new_django_project.urls'

WSGI_APPLICATION = 'new_django_project.wsgi.application'

TEMPLATE_DEBUG = DEBUG
SHOW_DEBUG_TOOLBAR = DEBUG


ADMINS = (('ta', 'atlantij@gmail.com'), )
MANAGERS = ADMINS

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_ROOT = os.path.join(BASE_DIR, 'static_prepared')
MEDIA_URL = '/media/'
STATIC_URL = '/static/'

ADMIN_MEDIA_PREFIX = '/static/admin/'


ALLOWED_HOSTS = ['*']

SECRET_KEY = '(nx07asda123dsfkllkqwe4t9kb^l1r82_0q24o%tjcikgq@w-ax@^qzk@$w7tzn!+y'

TIME_ZONE = 'Europe/Moscow'

SITE_ID = 1

LANGUAGE_CODE = "Ru-ru"
USE_I18N = True
USE_L10N = True

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFramnew_django_projecttionsMiddleware',

    'debug_toolbar.middleware.DebugToolbarMiddleware',

    'new_django_project.main.middleware.request.RequestMiddleware',

)

TEMPLATE_CONTEXT_PROCESSORS = (
    # default template context processors
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.static',

    'new_django_project.main.context_processors.registry',
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
    os.path.join(BASE_DIR, 'templates', 'admin'),
)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

INSTALLED_APPS = (
    'suit',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'debug_toolbar',
    'gunicorn',
    'south',
    'tinymce',
    'new_django_project.main',
    'new_django_project.accounts',
)

# AUTH_PROFILE_MODULE = 'accounts.UserProfile'
AUTH_USER_MODEL = 'accounts.User'
LOGIN_REDIRECT_URL = r'/'
LOGOUT_REDIRECT_URL = r'/accounts/login/'

# Sessions settings
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_AGE = 10 * 21 * 60  #In seconds


TINYMCE_JS_URL = os.path.join(MEDIA_URL, 'js/tiny_mce/tiny_mce.js')
TINYMCE_DEFAULT_CONFIG = {
    'plugins': "table, paste, searchreplace",
    'theme_advanced_toolbar_location': "top",
    'theme_advanced_toolbar_align': "left",
    'width': "640",
    'height': "120"
    #'theme': "advanced",
}
TINYMCE_SPELLCHECKER = False
TINYMCE_COMPRESSOR = False

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'some_example': {
            'handlers': ['console', 'mail_admins'],
            'level': 'INFO',
            'formatter': 'verbose'
        },
    }
}


DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]


def custom_show_debugtoolbar(request):
    if SHOW_DEBUG_TOOLBAR or '_secret_debug_' in request.GET:
        return True


DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': 'new_django_project.settings.custom_show_debugtoolbar',
    'ENABLE_STACKTRACES': True,
    'SHOW_TEMPLATE_CONTEXT': True,
}


SUIT_CONFIG = {
    'ADMIN_NAME': u'ЕОП',
    'HEADER_DATE_FORMAT': 'l, j. F Y',
    'HEADER_TIME_FORMAT': 'H:i',
    'SHOW_REQUIRED_ASTERISK': True,
    'CONFIRM_UNSAVED_CHANGES': True,
    'MENU_OPEN_FIRST_CHILD': True,
    'LIST_PER_PAGE': 50,
    'MENU': (
        {'label': u'Пользователи и группы', 'models': ('accounts.user', 'auth.group'), 'icon':'icon-user'},
        {'label': u'Основные объекты', 'app': 'main', 'icon':'icon-folder-open'},
    )
}