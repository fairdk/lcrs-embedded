"""
Here we put all the classes that run specific jobs
"""
import logging
import time

from . import models
from .system.dmesg import dmesg_analysis
from .system.lspci import lspci_analysis
from .system.smartctl import smartinfo
from .utils.job import Job


logger = logging.getLogger(__name__)


class ScanJob(Job):
    """
    Job that probes various hardware information stuff and returns once all
    the probing is done.
    """

    def job(self):

        # Store results
        scan_results = models.ScanResult()

        job_progress_map = [
            (lspci_analysis, 1),
            (dmesg_analysis, 1),
            (smartinfo, 1),
        ]

        total_progress_weight = sum(x[1] for x in job_progress_map)
        total_progress_weight = float(total_progress_weight)

        for job_func, progress in job_progress_map:
            job_func(scan_results)
            self.progress += progress / total_progress_weight


class FailJob(Job):
    """
    Purpose: testing
    """

    def job(self):
        raise Exception("I'm a failing thread, I died.")


class WaitJob(Job):
    """
    Purpose: testing
    """
    def __init__(self, *args, **kwargs):
        super(WaitJob, self).__init__(*args, **kwargs)

    def job(self, **kwargs):
        logger.debug(kwargs)
        wait_time = self.kwargs['wait_time']
        for x in range(wait_time):
            self.progress = float(x) / wait_time
            time.sleep(1)
