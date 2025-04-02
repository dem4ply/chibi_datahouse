import os


env = os.environ.get(
    'CHIBI_DATAHOUSE__ENVIRONMENT', 'local' ).lower()

is_production = env == 'production'

print( 'is_production: {}'.format( is_production ) )

from .base.prod import *  # noqa
from .base.prod import DEBUG  # noqa
from .database.prod import DATABASES  # noqa
from .installed_apps.prod import *  # noqa
from .middleware.prod import *  # noqa


if is_production:
    from .logger.prod import *  # noqa
else:
    from .logger.local import *  # noqa


from .rest_framework.prod import *  # noqa
from .cors.prod import *  # noqa


if is_production:
    from .elasticsearch.prod import *  # noqa
else:
    from .elasticsearch.local import *  # noqa


from .celery.prod import *  # noqa
#from .apis.prod import *  # noqa

DATABASES[ 'default' ][ 'CONN_MAX_AGE' ] = 0
