import logging
import os
import shlex
import subprocess

from functools import wraps

from .. import settings
from .job import Job


logger = logging.getLogger(__name__)


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
            job_id = instance.scheduler.add_job(JobType)
            instance.respond_job_id(job_id)
            return method(instance, *args, **kwargs)

        return wrapper

    return outer_wrapper


def thread_safe_method(lock_attr):

    def outer_wrapper(method):

        @wraps(method)
        def wrapper(instance, *args, **kwargs):
            lock = getattr(instance, lock_attr)
            lock.acquire()
            return_value = method(instance, *args, **kwargs)
            lock.release()
            return return_value
        return wrapper

    return outer_wrapper


def run_command_with_timeout(command, timeout=1, mock_in_test=False):
    """
    Runs a command, calling the decorated function with the results of the
    command.
    """

    def run_command():

        try:
            p = subprocess.run(
                shlex.split(command),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=timeout,
                check=True,
            )
            stdout = p.stdout.decode('utf-8')
            stderr = p.stderr.decode('utf-8')
            succeeded = p.returncode == 0

        except subprocess.TimeoutExpired:
            stdout = ""
            stderr = ""
            succeeded = False
            logger.error("Command timed out: {}".format(command))

        return stdout, stderr, succeeded

    def outer_rapper(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            # Ensure the default is always to mock when running in CI mode
            mock = (
                settings.TESTING and
                hasattr(wrapper, 'mock_output') and
                kwargs.pop('mock', mock_in_test or settings.IS_CI)
            )

            if not mock:
                stdout, stderr, succeeded = run_command()
            else:
                stdout, stderr, succeeded = wrapper.mock_output, "", True

            return func(
                *args,
                stdout=stdout,
                stderr=stderr,
                succeeded=succeeded,
                **kwargs
            )

        return wrapper

    return outer_rapper


def readfile(file_path, mock_in_test=False):
    """
    Runs a command, calling the decorated function with the results of the
    command.

    """

    def outer_rapper(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            """
            :param: mock_failure: If set, mocks stdout on failed command
            """

            mock_failure = kwargs.pop('mock_failure', None)

            # Ensure the default is always to mock when running in CI mode
            mock = (
                settings.TESTING and
                hasattr(wrapper, 'mock_output') and
                kwargs.pop('mock', mock_in_test or settings.IS_CI)
            )

            readable = True
            file_contents = ""

            if not mock:
                if os.access(file_path, os.R_OK):
                    file_contents = open(file_path).read()
                else:
                    readable = False
            elif mock_failure:
                file_contents = mock_failure
                readable = False
            else:
                file_contents = wrapper.mock_output

            return func(
                *args,
                file_contents,
                readable=readable,
                **kwargs
            )

        return wrapper

    return outer_rapper
