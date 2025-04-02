import os


#mysql
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ[ 'CHIBI_DATAHOUSE__DATABASE__NAME' ],
        'USER': os.environ[ 'CHIBI_DATAHOUSE__DATABASE__USER' ],
        'PASSWORD': os.environ[ 'CHIBI_DATAHOUSE__DATABASE__PASSWORD' ],
        'HOST': os.environ[ 'CHIBI_DATAHOUSE__DATABASE__HOST' ],
        'PORT': os.environ[ 'CHIBI_DATAHOUSE__DATABASE__PORT' ],
    },
}
