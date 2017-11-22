"""
Overwrite all harddrives
"""
import random
from ..utils.decorators import run_command
from ..models import HarddriveSample

#: Size of samples taken before and after overwrite
SAMPLE_SIZE = 512
FORMATTED_SIZE = 2312

def _readDrive(drive, offset, size):
    """
    Read <size> bytes from <drive> starting at <offset>.
    Returns the result as formatted by hexdump.
    """
    command = "hexdump -vx -s {} -n {} {}".format(offset, size, drive)
    @run_command(command)
    def read_drive_before(drive, stdout, stderr, succeeded):
        sample = HarddriveSample()
        if succeeded:
            if len(stdout) == FORMATTED_SIZE:
                sample.status = "Complete"
                sample.result = stdout
            else:
                sample.status = "Failed: Unexpected sample size"
                sample.result = ""
        else:
            sample.status = stderr
            sample.result = ""
        return sample
    return read_drive_before(drive)


def _isZero(sample):
    return sample.count('0') == len(sample)


def overwrite_disks(scan_result):
    """
    Overwrite each harddrive taking a random sample before and after.
    """
    for harddrive in scan_result.harddrives:
        offset = random.randrange(0, harddrive.capacity - SAMPLE_SIZE)
        harddrive.sample_random_offset = offset
        harddrive.sample_before = _readDrive(harddrive.dev, offset, SAMPLE_SIZE)
        # TODO: overwrite disk
        harddrive.sample_after = _readDrive(harddrive.dev, offset, SAMPLE_SIZE)
