"""
System invocation

class CommandNotAvailable(RuntimeError):
    pass


# Shell commands for the first iteration and functions for analyzing data
SCAN_ITERATION_1 = {
    "cat /proc/acpi/battery/BAT0/info": "analyze_battery_info",
}

#dd if=/dev/dvd of=/dev/null count=1 2>/dev/null; if [ $? -eq 0 ]; then echo "disk found"; else echo "no disk"; fi

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
