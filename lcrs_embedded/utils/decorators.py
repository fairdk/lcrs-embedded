from functools import wraps
from .job import Job


def threaded_api_request(JobType=Job):
    """
    Spawns a new thread and adds another job ID to the queue,
    """

    def outer_wrapper(method):

        @wraps(method)
        def wrapper(instance, *args, **kwargs):
            """
            :param: instance: JSONRequestHandler instance
            """
            job_id = instance.add_job(JobType)
            instance.respond_job_id(job_id)

        return wrapper

    return outer_wrapper


def thread_safe_method(lock_attr):

    def outer_wrapper(method):

        @wraps(method)
        def wrapper(instance, *args, **kwargs):
            lock = getattr(instance, lock_attr)
            lock.acquire()
            method(instance, *args, **kwargs)
            lock.release()
        return wrapper

    return outer_wrapper
