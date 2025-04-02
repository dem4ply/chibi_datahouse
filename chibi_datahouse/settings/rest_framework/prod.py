import os

import chibi_donkey as donkey
from chibi.snippet.dict import get_regex, lower_keys


rest_envars = donkey.inflate(
    lower_keys( get_regex(
        os.environ, r'CHIBI_DATAHOUSE__REST__.+' ) ) )[ 'chibi_datahouse' ][ 'rest' ]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'chibi_user.authentication.Token_simple_authentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        # 'rest_framework_xml.renderers.XMLRenderer',
        # 'rest_framework_yaml.renderers.YAMLRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        # 'rest_framework_xml.parsers.XMLParser',
        # 'rest_framework_yaml.parsers.YAMLParser',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.OrderingFilter',
    ),
    'DEFAULT_CONTENT_NEGOTIATION_CLASS':
        'rest_framework.negotiation.DefaultContentNegotiation',
    'EXCEPTION_HANDLER': 'chibi_django.exceptions.generic_exception_handler',
    'NON_FIELD_ERRORS_KEY': 'detail',
    'DEFAULT_VERSIONING_CLASS':
        'rest_framework.versioning.AcceptHeaderVersioning',
    'DEFAULT_VERSION': 'tigrinus',
    'ALLOWED_VERSIONS': ( 'tigrinus', ),
    'VERSION_PARAM': 'lanius',
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'DEFAULT_PAGINATION_CLASS':
        'chibi_django.pagination.Link_header_pagination',
    'PAGE_SIZE': int( rest_envars.get( 'page_size' ) )
}

