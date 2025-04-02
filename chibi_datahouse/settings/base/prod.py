import os
import json
from six.moves.urllib import request
from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.backends import default_backend


env = os.environ.get( 'CHIBI_DATAHOUSE__ENVIRONMENT', 'local' ).lower()

is_production = env == 'production'

PROJECT_NAME = 'chibi_datahouse'
TEST_MODE = bool( os.environ.get( 'CHIBI_DATAHOUSE__TEST_MODE', False ) )

SECRET_KEY = os.environ.get( 'CHIBI_DATAHOUSE__SECRET_KEY', '' )
DEBUG = not is_production

ALLOWED_HOSTS = [ '*' ]

ROOT_URLCONF = 'chibi_datahouse.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'chibi_datahouse.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
            'django.contrib.auth.password_validation.'
            'UserAttributeSimilarityValidator',
    },
    {
        'NAME':
            'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
            'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
            'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

BASE_DIR = os.path.dirname( os.path.dirname( os.path.abspath( __file__ ) ) )

STATIC_ROOT = os.path.join( BASE_DIR, 'staticfiles' )

#STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

AUTH_USER_MODEL = 'chibi_user.User'
AUTH_GROUP_MODEL = 'chibi_user.Group'
AUTH_PERMISSION_MODEL = 'chibi_user.Permission'

SESSION_ENGINE = 'django.contrib.sessions.backends.db'


AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)


#SECURE_SSL_REDIRECT = not DEBUG
#SECURE_PROXY_SSL_HEADER = ( 'HTTP_X_FORWARDED_PROTO', 'https' )


"""
AUTH0_DOMAIN = os.environ[ 'CHIBI_DATAHOUSE__AUTH0__DOMAIN' ]
API_IDENTIFIER = os.environ[ 'CHIBI_DATAHOUSE__AUTH0__IDENTIFIER' ]
PUBLIC_KEY = None
JWT_ISSUER = None

if AUTH0_DOMAIN:
    print( AUTH0_DOMAIN )
    json_url = request.urlopen(
        'https://' + AUTH0_DOMAIN + '/.well-known/jwks.json' )
    jwks = json.loads( json_url.read().decode( 'utf-8' ) )
    cert = "-----BEGIN CERTIFICATE-----\n{}\n-----END CERTIFICATE-----".format(
        jwks[ 'keys' ][0][ 'x5c' ][0] )
    certificate = load_pem_x509_certificate(
        cert.encode( 'utf-8' ), default_backend() )
    PUBLIC_KEY = certificate.public_key()
    JWT_ISSUER = 'https://' + AUTH0_DOMAIN + '/'

def jwt_get_username_from_payload_handler(payload):
    from chibi_user.models import User
    email = payload[ 'email' ]
    try:
        User.objects.get( email=email )
    except User.DoesNotExist:
        User.objects.create_user( email=email, username=email )
    return email

JWT_AUTH = {
    'JWT_PAYLOAD_GET_USERNAME_HANDLER': jwt_get_username_from_payload_handler,
    'JWT_PUBLIC_KEY': PUBLIC_KEY,
    'JWT_ALGORITHM': 'RS256',
    'JWT_AUDIENCE': API_IDENTIFIER,
    'JWT_ISSUER': JWT_ISSUER,
    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
}
"""
