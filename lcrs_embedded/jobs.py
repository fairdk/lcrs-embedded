"""
Here we put all the classes that run specific jobs
"""

from .utils.job import Job


class TestJob(Job):

    def run(self):
        raise Exception("I died")
