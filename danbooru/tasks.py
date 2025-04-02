from celery.utils.log import get_task_logger

from chibi_datahouse.tasks_class import Task_base
from chibi_datahouse.app_celery import chibi_datahouse_task as celery_task
from danbooru.scrapper import danbooru, Danbooru_post
from danbooru.serializers import Post as Post_serializer

from chibi_site import Chibi_site


logger = get_task_logger( 'chibi_datahouse.task.danbooru' )


@celery_task.task( bind=True, base=Task_base, ignore_result=True )
def debug_task( self, *args, **kw ):
    logger.debug(
        "execute task for debug",
        extra={ 'params': { 'args': args, 'kargs': kw } } )


@celery_task.task(
    bind=True, base=Task_base, ignore_results=True, max_retries=3 )
def scan_page( self, page=None, *args, **kw ):
    if page is None:
        page = danbooru
    else:
        page = danbooru( page )
    posts = page.images_sites
    for post in posts:
        scan_post.delay( str( post ) )

    scan_page.delay( str( page.next_page ) )


@celery_task.task(
    bind=True, base=Task_base, ignore_results=True, max_retries=3 )
def scan_post( self, post, *args, **kw ):
    post = Danbooru_post( post )
    serializer = Post_serializer( data=post.info )
    serializer.is_valid( raise_exception=True )
    model = serializer.save()
    return model.pk
