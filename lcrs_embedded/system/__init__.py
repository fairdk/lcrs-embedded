"""
System invocation

class CommandNotAvailable(RuntimeError):
    pass

S.M.A.R.T. data
hdparm
ATA secure erase possible?
ata secure erase
badblocks
wipe

# Shell commands for second iteration. Each command has a tuple (analyze function, command parser)
# for analyzing output and parsing the command (for possible inclusion of data from the first iteration)
SCAN_ITERATION_2 = {
    "echo %(sdX)s && hdparm -i /dev/%(sdX)s": ("analyze_hdparm", lambda com, hw: [com % {'sdX': key} for key in hw.get("Hard drives", {}).keys()]),
    "echo %(sdX)s && sdparm -q -p sn /dev/%(sdX)s": ("analyze_sdparm", lambda com, hw: [com % {'sdX': key} for key in hw.get("Hard drives", {}).keys()]),
    "echo %(sdX)s && blockdev --getsize64 /dev/%(sdX)s": ("analyze_blockdev", lambda com, hw: [com % {'sdX': key} for key in hw.get("Hard drives", {}).keys()]),
    "echo %(sdX)s && readlink -f /sys/block/%(sdX)s/": ("analyze_sysblock", lambda com, hw: [com % {'sdX': key} for key in hw.get("Hard drives", {}).keys()]),
}


def dmi_decode():
    pass
"""  # noqa
