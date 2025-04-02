import os

from celery.signals import setup_logging
import chibi_donkey as donkey
from chibi.snippet.dict import get_regex, lower_keys
from cmreslogging.handlers import CMRESHandler


app_name = os.environ.get( 'CHIBI_DATAHOUSE__APP_NAME' )

elastic_logger_env_vars = donkey.inflate(
    lower_keys( get_regex( os.environ, r'LOGGER__ELASTIC__.+' ) ) )

for e in elastic_logger_env_vars[ 'logger' ][ 'elastic' ].values():
    e[ 'auth_details' ] = ( e[ 'user' ], e[ 'password' ], )
    e[ 'auth_type' ] = CMRESHandler.AuthType.BASIC_AUTH
    # e[ 'ca_certs' ] = certifi.where()
    e[ 'class' ] = 'cmreslogging.handlers.CMRESHandler'
    e[ 'flush_frequency_in_sec' ] = int( e[ 'flush_frequency_in_sec' ] )
    e[ 'hosts' ] = [ e[ 'hosts' ] ]
    e[ 'use_ssl' ] = True
    e[ 'verify_ssl' ] = True

    e[ 'es_additional_fields' ] = {
        'app': app_name, 'tags': [ 'reader_moe', app_name ] }

    if e[ 'index_name_frequency' ] == 'monthly':
        e[ 'index_name_frequency' ] = CMRESHandler.IndexNameFrequency.MONTHLY
    else:
        raise NotImplementedError
    e.pop( 'user', None )
    e.pop( 'password', None )

handlers = {
    'console': {
        'class': 'logging.StreamHandler',
        'formatter': 'verbose',
        'stream': 'ext://sys.stdout',
    },
}
handlers.update( elastic_logger_env_vars[ 'logger' ][ 'elastic' ] )

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': handlers,
    'formatters': {
        'verbose': {
            'format':
                '%(levelname)s %(asctime)s %(name)s '
                '%(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(name)s %(asctime)s %(message)s'
        },
    },
    'root': {
        'handlers': [ 'console', 'elastic_log' ],
        'level': os.getenv( 'DJANGO_LOG_LEVEL', 'INFO' ),
        'propagate': True,
    },
    'loggers': {
        'django.request': {
            'level': os.getenv(
                'DJANGO_LOG_LEVEL__DJANGO__REQUESTS', 'WARNING' ),
        },
        'requests': {
            'level': os.getenv( 'DJANGO_LOG_LEVEL__REQUESTS', 'WARNING' ),
        },
        'elasticsearch': {
            'level': os.getenv( 'DJANGO_LOG_LEVEL__ELASTICSEARCH', 'WARNING' ),
        },
    }
}


@setup_logging.connect
def configure_logging(sender=None, **kwargs):
    import logging
    import logging.config
    logging.config.dictConfig( LOGGING )
