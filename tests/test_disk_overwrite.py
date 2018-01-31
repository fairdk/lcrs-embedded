import pytest
import logging
import time
import os

from lcrs_embedded.models import ScanResult, Harddrive
from . import *  # noqa  # This loads the fixtures that are in __init__.py

logger = logging.getLogger(__name__)


def writeXes(fileName, count):
    testFile = open(fileName, "w")
    testFile.write(count * "x")
    testFile.close()


def test_overwrite(runserver):
    """
    Test sampling of disk
    """
    from lcrs_embedded.system.disk_overwrite import overwrite_disks
    logger.info("Testing ???")
    testFileName = "testDiskOverwrite.txt"
    writeXes(testFileName, 2000)
    test_harddrives = []
    test_harddrives.append(Harddrive(dev=testFileName, capacity=2000))
    scan_result = ScanResult(
        harddrives=test_harddrives
    )
    overwrite_disks(scan_result)
    assert scan_result.harddrives[0].sample_before.status == "Complete"
    assert not scan_result.harddrives[0].sample_random_offset is None
    os.remove(testFileName)


def test_too_small_disk(runserver):
    """
    Test that overwrite fails if device is less than 512 bytes.
    """
    from lcrs_embedded.system.disk_overwrite import overwrite_disks
    logger.info("Testing that overwrite fails if device is less than 512 bytes")
    testFileName = "testDiskOverwrite.txt"
    writeXes(testFileName, 300)
    test_harddrives = []
    test_harddrives.append(Harddrive(dev=testFileName, capacity=2000)) # Note capacity is less than 2000
    scan_result = ScanResult(
        harddrives=test_harddrives
    )
    overwrite_disks(scan_result)
    assert scan_result.harddrives[0].sample_before.result == ""
    assert scan_result.harddrives[0].sample_before.status == "Failed: Unexpected sample size"
    os.remove(testFileName)


def test_missing_disk(runserver):
    """
    Test that disk sample fails on missing drive
    """
    from lcrs_embedded.system.disk_overwrite import overwrite_disks
    logger.info("Testing that disk sample fails on missing drive")
    testFileName = "testDiskOverwrite.txt"
    test_harddrives = []
    test_harddrives.append(Harddrive(dev=testFileName, capacity=2000))
    scan_result = ScanResult(
        harddrives=test_harddrives
    )
    overwrite_disks(scan_result)
    assert scan_result.harddrives[0].sample_before.result == ""
    assert "No such file or directory" in scan_result.harddrives[0].sample_before.status
