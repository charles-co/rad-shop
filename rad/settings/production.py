from .base import *

DEBUG = False

BASE_URL = 'rad-simulation.herokuapp.com'

ALLOWED_HOSTS = ['rad-simulation.herokuapp.com']

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER     = os.environ.get("GMAIL_EMAIL")
EMAIL_HOST_PASSWORD = os.environ.get("GMAIL_PASSWORD")
EMAIL_PORT = 465
EMAIL_USE_SSL = True # Yes for Gmail
DEFAULT_FROM_EMAIL = "Rad | Shop < " + os.environ.get("GMAIL_EMAIL") + " >"

import dj_database_url

db_from_env = dj_database_url.config(conn_max_age=600) #postgreSQL Database in heroku
DATABASES['default'].update(db_from_env)


STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles/')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

CORS_REPLACE_HTTPS_REFERER      = True
HOST_SCHEME                     = "https://"
SECURE_PROXY_SSL_HEADER         = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT             = True
SESSION_COOKIE_SECURE           = True
CSRF_COOKIE_SECURE              = True
SECURE_HSTS_INCLUDE_SUBDOMAINS  = True
SECURE_HSTS_SECONDS             = 1000000
SECURE_FRAME_DENY               = True