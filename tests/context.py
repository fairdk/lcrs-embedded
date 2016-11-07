import logging
from contextlib import contextmanager
from threading import ThreadError

logger = logging.getLogger(__name__)


@contextmanager
def assert_no_thread_exceptions():
    yield
    from lcrs_embedded import settings
    if not settings.EXCEPTION_QUEUE.empty():
        logger.error("Ohs nos a subthread failed")
        while not settings.EXCEPTION_QUEUE.empty():
            logger.error(settings.EXCEPTION_QUEUE.get_nowait())
        raise ThreadError("Bye bye")
