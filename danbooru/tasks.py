from celery.utils.log import get_task_logger
from celery.schedules import crontab

from chibi_datahouse.tasks_class import Task_base
from chibi_datahouse.app_celery import chibi_datahouse_task as celery_task
from chibi_requests import Chibi_url
from danbooru.scrapper import danbooru, Danbooru_post, Danbooru
from danbooru.serializers import Post as Post_serializer
from danbooru.models import Post as Post_model

from chibi_site import Chibi_site


logger = get_task_logger( 'chibi_datahouse.task.danbooru' )


@celery_task.task( bind=True, base=Task_base, ignore_result=True )
def debug_task( self, *args, **kw ):
    logger.debug(
        "execute task for debug",
        extra={ 'params': { 'args': args, 'kargs': kw } } )


@celery_task.task(
    bind=True, base=Task_base, ignore_results=True, max_retries=3,
    rate_limit='30/m' )
def scan_page( self, page=None, *args, **kw ):
    if page is None:
        page = danbooru
    else:
        page = Danbooru( page )
    logger.info( f"leyendo '{page}'" )
    posts = page.images_sites
    for post in posts:
        should_scan_post.delay( str( post ) )

    scan_page.delay( str( page.next_page ) )


@celery_task.task(
    bind=True, base=Task_base, ignore_results=True, )
def should_scan_post( self, post_url, *args, **kw ):
    url = Chibi_url( post_url )
    trash, pk = url.url.rsplit( '/', 1 )
    if not Post_model.exists( id=pk ):
        scan_post.delay( post_url )


@celery_task.task(
    bind=True, base=Task_base, ignore_results=True, max_retries=3,
    rate_limit='20/m' )
def scan_post( self, post, *args, **kw ):
    post = Danbooru_post( post )
    logger.info( f"leyendo '{post}'" )
    serializer = Post_serializer( data=post.info )
    serializer.is_valid( raise_exception=True )
    model = serializer.save()
    return model.pk


@celery_task.on_after_configure.connect
def setup_periodic_tasks( sender, **kw ):
    # sender.add_periodic_task( 10.0, test.s( 'hello' ), name='add every 10' )
    # # Calls test( 'hello' ) every 30 seconds.
    # # It uses the same signature of previous task, an explicit name is
    # # defined to avoid this task replacing the previous one defined.
    # sender.add_periodic_task( 30.0, test.s( 'hello' ), name='add every 30' )
    # # Calls test( 'world' ) every 30 seconds
    # sender.add_periodic_task( 30.0, test.s( 'world' ), expires=10 )

    sender.add_periodic_task(
        crontab( hour=12, minute=0 ),
        scan_page.s(),
    )
