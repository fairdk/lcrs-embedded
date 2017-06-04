import pytest
import logging
import time

from lcrs_embedded.models import ScanResult
from . import *  # noqa  # This loads the fixtures that are in __init__.py

logger = logging.getLogger(__name__)


def test_cpu_load(runserver):
    """
    Test duration of load of CPU.
    """
    from lcrs_embedded.system.cpu_load import multiple_processes_load_cpu
    logger.info("Testing duration of load of CPU...")
    duration_in_seconds = 1
    startTime = int(time.time())
    scan_result = ScanResult(
        processor_cores=1
    )
    multiple_processes_load_cpu(scan_result, duration_in_seconds)
    actual_duration = int(time.time()) - startTime
    assert actual_duration >= duration_in_seconds
    assert actual_duration <= duration_in_seconds + 1
