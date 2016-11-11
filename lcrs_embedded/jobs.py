"""
Here we put all the classes that run specific jobs
"""

from . import models
from .system.dmesg import dmesg_analysis
from .system.lspci import lspci_analysis
from .utils.job import Job


class ScanJob(Job):
    """
    Job that probes various hardware information stuff and returns once all
    the probing is done.
    """

    def job(self):
        scan_results = models.ScanResult()
        lspci_analysis(scan_results)
        self.progress = 0.5
        dmesg_analysis(scan_results)
        self.progress = 1.0


class FailJob(Job):

    def job(self):
        raise Exception("I'm a failing thread, I died.")
