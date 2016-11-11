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
import logging
import re

from .utils.decorators import run_command_with_timeout

logger = logging.getLogger(__name__)


@run_command_with_timeout("lspci")
def lspci_analysis(scan_results, stdout, stderr, succeeded):
    """
    :param: scan_result: A ``ScanResult`` instance.
    """

    if not succeeded:
        return

    p = re.compile(r"VGA compatible controller\:\s*(.+)\s*$", re.M | re.I)
    m = p.search(stdout)
    if m:
        scan_results.graphics_controller = m.group(1)

    p = re.compile(r"Network controller\:\s*(.+)\s*$", re.I | re.M)
    m = p.search(stdout)
    if m:
        scan_results.wifi = m.group(1)

    p = re.compile(r"Ethernet controller\:\s*(.+)\s*$", re.M | re.I)
    m = p.search(stdout)
    if m:
        scan_results.ethernet = m.group(1)

    p = re.compile(r"USB controller\:\s*(.+)\s*$", re.M | re.I)
    m = p.search(stdout)
    if m:
        scan_results.usb_controller = m.group(1)
        scan_results.has_usb = True

lspci_analysis.test_input = """
00:00.0 Host bridge: Intel Corporation 2nd Generation Core Processor Family DRAM Controller (rev 09)
00:02.0 VGA compatible controller: Intel Corporation 2nd Generation Core Processor Family Integrated Graphics Controller (rev 09)
00:16.0 Communication controller: Intel Corporation 6 Series/C200 Series Chipset Family MEI Controller #1 (rev 04)
00:19.0 Ethernet controller: Intel Corporation 82579LM Gigabit Network Connection (rev 04)
00:1a.0 USB controller: Intel Corporation 6 Series/C200 Series Chipset Family USB Enhanced Host Controller #2 (rev 04)
00:1b.0 Audio device: Intel Corporation 6 Series/C200 Series Chipset Family High Definition Audio Controller (rev 04)
00:1c.0 PCI bridge: Intel Corporation 6 Series/C200 Series Chipset Family PCI Express Root Port 1 (rev b4)
00:1c.1 PCI bridge: Intel Corporation 6 Series/C200 Series Chipset Family PCI Express Root Port 2 (rev b4)
00:1c.3 PCI bridge: Intel Corporation 6 Series/C200 Series Chipset Family PCI Express Root Port 4 (rev b4)
00:1c.4 PCI bridge: Intel Corporation 6 Series/C200 Series Chipset Family PCI Express Root Port 5 (rev b4)
00:1c.6 PCI bridge: Intel Corporation 6 Series/C200 Series Chipset Family PCI Express Root Port 7 (rev b4)
00:1d.0 USB controller: Intel Corporation 6 Series/C200 Series Chipset Family USB Enhanced Host Controller #1 (rev 04)
00:1f.0 ISA bridge: Intel Corporation QM67 Express Chipset Family LPC Controller (rev 04)
00:1f.2 SATA controller: Intel Corporation 6 Series/C200 Series Chipset Family 6 port SATA AHCI Controller (rev 04)
00:1f.3 SMBus: Intel Corporation 6 Series/C200 Series Chipset Family SMBus Controller (rev 04)
03:00.0 Network controller: Intel Corporation Centrino Advanced-N 6205 [Taylor Peak] (rev 34)
0d:00.0 System peripheral: Ricoh Co Ltd PCIe SDXC/MMC Host Controller (rev 07)
0e:00.0 USB controller: NEC Corporation uPD720200 USB 3.0 Host Controller (rev 04)
"""  # noqa

lspci_analysis.expected_results = {
    'wifi': (
        "Intel Corporation Centrino Advanced-N 6205 [Taylor Peak] (rev 34)"),
    'ethernet': (
        "Intel Corporation 82579LM Gigabit Network Connection (rev 04)"),
}
