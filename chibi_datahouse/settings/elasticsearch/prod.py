import os

import certifi
import chibi_donkey as donkey
from chibi.snippet.dict import get_regex, lower_keys
from elasticsearch_dsl.connections import connections


elastic_env_vars = donkey.inflate(
    lower_keys( get_regex( os.environ, r'ELASTIC__.+' ) ) )[ 'elastic' ]

for e in elastic_env_vars.values():
    e[ 'hosts' ] = [ e[ 'hosts' ] ]
    e[ 'http_auth' ] = ( e[ 'user' ], e[ 'password' ] )
    e[ 'ca_certs' ]: certifi.where()
    e[ 'use_ssl' ]: True
    e[ 'verify_certs' ]: True
    e[ 'timeout' ] = int( e[ 'timeout' ] )


connections.configure( **elastic_env_vars )
