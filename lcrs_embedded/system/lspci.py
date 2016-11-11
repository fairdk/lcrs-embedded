import logging
import re

from ..utils.decorators import run_command_with_timeout

logger = logging.getLogger(__name__)


@run_command_with_timeout("lspci")
def lspci_analysis(scan_result, stdout, stderr, succeeded):
    """
    :param: scan_result: A ``ScanResult`` instance.
    """

    if not succeeded:
        return

    p = re.compile(r"VGA compatible controller\:\s*(.+)\s*$", re.M | re.I)
    m = p.search(stdout)
    if m:
        scan_result.graphics_controller = m.group(1)

    p = re.compile(r"Network controller\:\s*(.+)\s*$", re.I | re.M)
    m = p.search(stdout)
    if m:
        scan_result.wifi = m.group(1)

    p = re.compile(r"Ethernet controller\:\s*(.+)\s*$", re.M | re.I)
    m = p.search(stdout)
    if m:
        scan_result.ethernet = m.group(1)

    p = re.compile(r"USB controller\:\s*(.+)\s*$", re.M | re.I)
    m = p.search(stdout)
    if m:
        scan_result.usb_controller = m.group(1)
        scan_result.has_usb = True

lspci_analysis.mock_output = """
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
