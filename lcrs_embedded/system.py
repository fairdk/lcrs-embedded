"""
System invocation

class CommandNotAvailable(RuntimeError):
    pass


# Shell commands for the first iteration and functions for analyzing data
SCAN_ITERATION_1 = {
    "/usr/sbin/lspci": "analyze_lspci_data",
    "dmesg": "analyze_dmesg_data",
    "dmidecode -s system-manufacturer": "analyze_dmidecode_manufacturer",
    "dmidecode -s system-uuid": "analyze_dmidecode_uuid",
    "dmidecode -s system-serial-number": "analyze_dmidecode_system_sn",
    "dmidecode -s baseboard-serial-number": "analyze_dmidecode_bios_sn",
    "dmidecode -t system": "analyze_dmidecode_system",
    "dmidecode --string chassis-type": "analyze_dmidecode_chassis_type",
    "dmidecode -t memory": "analyze_dmidecode_memory",
    "cat /proc/meminfo": "analyze_meminfo_data",
    "cat /proc/cpuinfo": "analyze_cpu_data",
    "cat /proc/sys/dev/cdrom/info": "analyze_cdrom_info",
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
