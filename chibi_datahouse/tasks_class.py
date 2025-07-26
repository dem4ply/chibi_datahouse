from celery.utils.log import get_task_logger

from chibi_datahouse.app_celery import chibi_datahouse_task as celery_task


logger = get_task_logger( 'celery.task.chibi_datahouse' )


class Task_base( celery_task.Task ):
    abstract = True

    def on_success( self, retval, task_id, args, kwargs ):
        extra = {
            'task_id': task_id,
            'task_name': self.name,
            'params': { 'args': args, 'kargs': kwargs },
        }
        logger.info( f"sucess task {self.name} ( {task_id} )", extra=extra )
        super().on_success( retval, task_id, args, kwargs )

    def on_retry( self, exc, task_id, args, kwargs, einfo ):
        extra = {
            'task_id': task_id,
            'task_name': self.name,
            'params': { 'args': args, 'kargs': kwargs },
        }
        logger.error(
            f"retry task {self.name} ( {task_id} )",
            exc_info=exc, extra=extra )
        super().on_retry( exc, task_id, args, kwargs, einfo )

    def on_failure( self, exc, task_id, args, kwargs, einfo ):
        extra = {
            'task_id': task_id,
            'task_name': self.name,
            'params': { 'args': args, 'kargs': kwargs },
        }
        if self.request.retries >= self.max_retries:
            logger.error(
                f"fail task {self.name} ( {task_id} )",
                exc_info=exc, extra=extra )
            super().on_failure( task_id, exc, args, kwargs, einfo )
        else:
            logger.error(
                f"retry task {self.name} ( {task_id} )",
                exc_info=exc, extra=extra )
            self.retry()
