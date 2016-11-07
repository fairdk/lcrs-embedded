"""
Here we put all the classes that run specific jobs
"""

from .utils.job import Job


class FailJob(Job):

    def job(self):
        raise Exception("I'm a failing thread, I died.")
