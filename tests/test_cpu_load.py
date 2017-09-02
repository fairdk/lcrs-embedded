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
    from lcrs_embedded.system.cpu_load import cpu_load
    logger.info("Testing duration of load of CPU with two cores")
    duration_in_seconds = 1
    startTime = time.time()
    scan_result = ScanResult(
        processor_threads=2
    )
    cpu_load(scan_result, duration_in_seconds)
    actual_duration = time.time() - startTime
    assert actual_duration >= duration_in_seconds
    assert actual_duration <= duration_in_seconds + 1
    assert scan_result.processor_load_status == "Complete"

def test_timed_cpu_load(runserver):
    """
    Test duration of load of CPU with a call in same process.
    """
    from lcrs_embedded.system.cpu_load import timed_cpu_load
    logger.info("Testing duration of load of CPU with one core")
    duration_in_seconds = 3
    startTime = time.time()
    endTime = startTime + duration_in_seconds
    timed_cpu_load(endTime)
    actual_duration = time.time() - startTime
    assert actual_duration >= duration_in_seconds
    assert actual_duration <= duration_in_seconds + 1
