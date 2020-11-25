"""
Django settings for rad project.

Generated by 'django-admin startproject' using Django 3.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import django_heroku
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(os.path.join(__file__, os.pardir))))
TEMPLATE_DIR = os.path.join(BASE_DIR,'templates')

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")
SITE_ID = 1
AUTH_USER_MODEL = 'accounts.User'
# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_HOST_USER     = os.environ.get("GMAIL_EMAIL")
# EMAIL_HOST_PASSWORD = os.environ.get("GMAIL_PASSWORD")
# EMAIL_PORT = 465
# EMAIL_USE_SSL = True # Yes for Gmail
# DEFAULT_FROM_EMAIL = "Rad | Shop os.environ.get("GMAIL_EMAIL")"
# BASE_URL = 'http://192.168.43.184:8000'

LOGIN_URL = 'accounts:login'
LOGIN_URL_REDIRECT = 'shop:shop-index'
LOGOUT_URL = '/logout/'
LOGOUT_REDIRECT_URL = 'accounts:login'

PASSWORD_RESET_TIMEOUT_DAYS = 3

MANAGERS = (
    ('Charles Oraegbu', "ch4rles.co@gmail.com"),
)

ADMINS = MANAGERS

# ALLOWED_HOSTS = ['192.168.43.184', '127.0.0.1', '172.20.10.4']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.sites',
    'django.contrib.redirects',
    'django.contrib.flatpages',

    'shop',
    'menu',
    'contents',
    'cart',
    'accounts',
    'billing',
    'addresses',
    'orders',


    'mptt',
    'taggit',
    'crispy_forms',
    'colorfield',
    'admin_honeypot',
    'rest_framework',
    'sorl.thumbnail',
    'rest_framework_recursive',
    'generic_relations',
    'django_celery_beat',
    'sorl_thumbnail_serializer',
    'tinymce',
    'phonenumber_field',
    'whitenoise.runserver_nostatic',
    'nested_admin',
]
# PHONENUMBER_DB_FORMAT = 'E164'
# PHONENUMBER_DEFAULT_REGION = 'NG'
CELERY_BROKER_URL = 'amqp://localhost'

TINYMCE_DEFAULT_CONFIG ={
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 20,
    'selector': 'textarea',
    'theme': 'silver',
    'plugins': '''
                textcolor save link preview contextmenu
                table lists fullscreen insertdatetime nonbreaking
                contextmenu directionality searchreplace wordcount
                visualblocks visualchars fullscreen autolink lists 
                charmap hr anchor pagebreak
                ''',
    'toolbar1': '''
                fullscreen preview bold italic underline | fontselect, 
                fontsizeselect | forecolor backcolor | alignleft alignright |
                aligncenter alignjustify | indent outdent | bullist numlist table |
                | link | 
                ''',
    'toolbar2': '''
                visualblocks visualchars |
                charmap hr pagebreak nonbreaking anchor |
                ''',
    'contextmenu': 'formats | link',
    'menubar': True,
    'statusbar': True,
}
TINYMCE_SPELLCHECKER = True

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
]

ROOT_URLCONF = 'rad.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cart.context_processors.cart',
                'rad.context_processors.debug',
            ],
            'libraries': {
                'extras': 'templatetags.extras',
            },
        },
    },
]

WSGI_APPLICATION = 'rad.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

CART_SESSION_ID = 'cart' 
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# STATIC_URL = '/static/'
# # STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, 'static/'),
# )

MEDIA_URL ='/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

