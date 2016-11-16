"""
Functions that read virtual files in /proc
"""
import logging
import re

from ..utils.decorators import readfile


logger = logging.getLogger(__name__)


@readfile("/proc/meminfo", mock_in_test=False)
def meminfo(scan_result, file_contents, readable):
    """
    Reads memory information, but only in case DMI data collection has not
    produced a reliable memory_total.
    """

    if not readable:
        logger.critical("Couldn't read /proc/meminfo")
        return

    "If a reliable number has been produced..."
    if scan_result.memory_total and scan_result.memory_total >= 256:
        return

    p = re.compile(r"^MemTotal:\s+(\d+)", re.I)
    m = p.search(file_contents)
    if m:
        scan_result.memory_total = int(m.group(1)) // 1024


meminfo.mock_output = """
MemTotal:        8054964 kB
MemFree:         1637080 kB
MemAvailable:    2628620 kB
Buffers:          174448 kB
Cached:          1384896 kB
SwapCached:        48916 kB
Active:          4411824 kB
Inactive:        1358492 kB
Active(anon):    3813984 kB
Inactive(anon):   941248 kB
Active(file):     597840 kB
Inactive(file):   417244 kB
Unevictable:         144 kB
Mlocked:             144 kB
SwapTotal:      16381948 kB
SwapFree:       15501316 kB
Dirty:               564 kB
Writeback:             0 kB
AnonPages:       4195128 kB
Mapped:           529588 kB
Shmem:            544260 kB
Slab:             339740 kB
SReclaimable:     279732 kB
SUnreclaim:        60008 kB
KernelStack:       13616 kB
PageTables:        55396 kB
NFS_Unstable:          0 kB
Bounce:                0 kB
WritebackTmp:          0 kB
CommitLimit:    20409428 kB
Committed_AS:   11498984 kB
VmallocTotal:   34359738367 kB
VmallocUsed:           0 kB
VmallocChunk:          0 kB
HardwareCorrupted:     0 kB
AnonHugePages:   1562624 kB
CmaTotal:              0 kB
CmaFree:               0 kB
HugePages_Total:       0
HugePages_Free:        0
HugePages_Rsvd:        0
HugePages_Surp:        0
Hugepagesize:       2048 kB
DirectMap4k:      759424 kB
DirectMap2M:     7510016 kB
"""
meminfo.expected_results = {
    'memory_total': 7866,
}
