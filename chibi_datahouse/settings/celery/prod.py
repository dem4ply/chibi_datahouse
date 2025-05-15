import os

from kombu import Exchange, Queue
# from celery.schedules import crontab
# from datetime import timedelta


user = os.environ[ 'CHIBI_DATAHOUSE__RABBITMQ__USER' ]
password = os.environ[ 'CHIBI_DATAHOUSE__RABBITMQ__PASSWORD' ]
vhost = os.environ[ 'CHIBI_DATAHOUSE__RABBITMQ__VHOST' ]
port = os.environ[ 'CHIBI_DATAHOUSE__RABBITMQ__PORT' ]
domain = os.environ[ 'CHIBI_DATAHOUSE__RABBITMQ__DOMAIN' ]
celery_url = f"amqp://{user}:{password}@{domain}:{port}/{vhost}"


CELERY_BROKER_URL = celery_url
# CELERY_RESULT_BACKEND = celery_url
CELERY_RESULT_BACKEND = 'rpc://'

# CELERY_TASK_DEFAULT_RATE_LIMIT = '5/s'

CELERY_TASK_ANNOTATIONS = { }

# beat_schedule = 'djcelery.schedulers.DatabaseScheduler'

CELERY_TASK_QUEUES = (
    Queue(
        'chibi_datahouse.default',
        Exchange( 'task', 'topic' ),
        routing_key='default' ),
    Queue(
        'debug', Exchange( 'task_debug', 'topic' ), routing_key='*.debug.*' ),
    Queue(
        'chibi_datahouse.danbooru',
        Exchange( 'task', 'topic' ),
        routing_key='danbooru' ),
)

CELERY_TASK_DEFAULT_QUEUE = 'chibi_datahouse.default'
CELERY_TASK_DEFAULT_EXCHANGE = "tasks"
CELERY_TASK_DEFAULT_EXCHANGE_TYPE = "topic"
CELERY_TASK_DEFAULT_ROUTING_KEY = "task.default"

CELERY_TASK_ROUTES = {
    'chibi_datahouse.default': {
        'binding_key': 'task.#',
    },
    'chibi_datahouse.tasks.debug_task': {
        'queue': 'debug',
        'binding_key': 'task.debug.*',
        'exchange': 'task_debug'
    },
    'danbooru.tasks.*': {
        'queue': 'chibi_datahouse.danbooru',
        'binding_key': 'task.#',
        #'exchange': 'danbooru'
    }
}

CELERY_BEAT_SCHEDULE = { }

CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'

CELERY_ALWAYS_EAGER = False
CELERY_TASK_ALWAYS_EAGER = False
