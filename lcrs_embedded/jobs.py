"""
Here we put all the classes that run specific jobs
"""

from .utils.job import Job


class ScanJob(Job):
    """
    Job that probes various hardware information stuff and returns once all
    the probing is done.
    """

    def job(self):
        self.progress = 1.0


class FailJob(Job):

    def job(self):
        raise Exception("I'm a failing thread, I died.")
