#!/usr/bin/env python3
import logging
import sys
import threading
from queue import Queue

from lcrs_embedded.utils.decorators import (thread_safe_method,
                                            threaded_api_request)

from . import __version__, jobs, settings
from .utils.http import JSONRequestHandler, SimpleServer

logger = logging.getLogger(__name__)


__active = True


class Scheduler:
    """
    NB! Call init_mixin in the __init__ of the inheritor
    """

    def __init__(self):
        logger.debug("Initialized a scheduler")
        self.job_id_counter = 0
        self.jobs = {}
        self.job_ids = []
        self.job_lock = threading.RLock()

    def job_id(self):
        """
        This method isn't tread safe
        """
        _job_id = self.job_id_counter + 1
        self.job_id_counter = _job_id
        self.job_ids.append(_job_id)
        return _job_id

    @thread_safe_method("job_lock")
    def add_job(self, JobType, *args, **kwargs):
        output_queue = Queue()
        exception_queue = settings.EXCEPTION_QUEUE
        job_id = self.job_id()
        job_thread = JobType(
            output_queue,
            exception_queue,
            job_id,
            target=lambda: logger.debug("Called an empty target"),
            args=args,
            kwargs=kwargs
        )
        job_thread.setDaemon(True)
        job_thread.start()
        self.jobs[job_id] = {
            'job': job_thread,
            'output_queue': output_queue,
        }
        return job_id


scheduler = Scheduler()


class LCRSRequestHandler(JSONRequestHandler):
    """
    This is where post requests are handled. A request for /api/v1/test will
    resolve to calling api_test() - methods are responsible for generating
    their own responses however they want.

    All this might seem simpler done with high-level frameworks like Tornado or
    Klein but we try to manage a minimal stack by using built-in Python
    libraries.
    """

    server_version = "LCRS/" + __version__
    static_srv = settings.HTTP_SRV_PATH

    def __init__(self, *args, **kwargs):
        self.scheduler = scheduler
        super(LCRSRequestHandler, self).__init__(*args, **kwargs)

    @threaded_api_request(jobs.FailJob)
    def api_fail(self, **kwargs):
        """
        For testing purposes, here's a call that always fails. We need to be
        sure that tests also fail in that case.
        """
        logger.debug('api_fail called, kwargs: {}'.format(kwargs))


def serve(port=8000, host='0.0.0.0'):
    global __active
    server = SimpleServer(('0.0.0.0', port), LCRSRequestHandler)
    logger.info(
        "Serving HTTP traffic on http://{host}:{port}".format(
            host=host, port=port
        )
    )
    try:
        while __active:
            sys.stdout.flush()
            server.handle_request()

    except KeyboardInterrupt:
        logger.info(
            "User stopped server"
        )


def stop():
    global __active
    logger.info(
        "Asking HTTP server to stop"
    )
    __active = False
