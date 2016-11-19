"""
S.M.A.R.T.

smartctl controls the Self-Monitoring, Analysis and Reporting Technology
(SMART) system built into most ATA/SATA and SCSI/SAS hard drives and solid-
state drives. The purpose of SMART is to monitor the reliability of the hard
drive and predict drive failures, and to carry out different types of drive
self-tests. smartctl also supports some features not related to SMART. This
version of smartctl is compatible with ACS-3, ACS-2, ATA8-ACS, ATA/ATAPI-7 and
earlier standards (see REFERENCES below).
"""
import logging
import re

from ..utils.decorators import run_command

logger = logging.getLogger(__name__)


def fetch_rows(scan_result, stdout, row_map, type_map=None):
    """
    Reused routine for fetching stuff from dmidecode -t <type> output
    """

    if not type_map:
        type_map = {}

    for row, attr in row_map.items():
        p = re.compile(r"^{row}:\s*(.+)\s*$".format(row=row), re.I | re.M)
        m = p.search(stdout)
        if m:
            match = m.group(1)
            logger.debug("Found S.M.A.R.T. info {}: {}".format(row, match))
            setattr(scan_result, attr, match)

    for attr, func in type_map.items():
        if scan_result[attr]:
            scan_result[attr] = func(scan_result[attr])


def clean_user_capacity(val):
    # Cleans a value like "250,053,931,008 bytes [250 GB]"

    val = val.split("bytes")

    if len(val) == 1:
        return None

    p = re.compile(r"\d")
    val = "".join(x for x in p.findall(val[0]) or [])
    val = int(val) if val else None
    return val


def _smartinfo_drive(drive):
    """
    Analyzes the "INFORMATION SECTION" of smartctl to determine properties of
    the remaining "SMART DATA SECTION".
    """

    global smart_mock_output

    command = "smartctl -i /dev/{}".format(drive.dev)

    @run_command(command, mock_in_test=True, ignore_fail=True)
    def _smart_meta(drive, stdout, stderr, succeeded):
        """
        default_mock = True because dmidecode needs root privileges
        """
        drive.smart_raw = stdout
        row_map = {
            'Serial Number': 'serial',
            'Device Model': 'model',
            'User Capacity': 'capacity',
            'Form Factor': 'form_factor',
            'Rotation Rate': 'is_ssd',
            'Device is': 'smart_well_known',
        }
        type_map = {
            'capacity': clean_user_capacity,
            'is_ssd': lambda s: "Solid State Device" in s,
            'smart_well_known': lambda s: "In smartctl database" in s
        }
        fetch_rows(drive, stdout, row_map, type_map=type_map)

        # Because 'SMART support is' appears twice
        row = 'SMART support is'
        p = re.compile(r"^{row}:\s*(.+)\s*$".format(row=row), re.I | re.M)
        ms = p.finditer(stdout)
        for m in ms:
            match = m.group(1)
            logger.debug("Found S.M.A.R.T. data for {}: {}".format(row, match))
            if 'available' in match.lower():
                drive.smart_available = True
            if 'enabled' in match.lower():
                drive.smart_enabled = True

    _smart_meta.mock_output = smart_mock_output

    _smart_meta(drive)


def smartinfo(scan_result, *args, **kwargs):

    for drive in scan_result.harddrives:

        _smartinfo_drive(drive)


smart_mock_output = """
smartctl 6.5 2016-01-24 r4214 [x86_64-linux-4.4.0-38-generic] (local build)
Copyright (C) 2002-16, Bruce Allen, Christian Franke, www.smartmontools.org

=== START OF INFORMATION SECTION ===
Model Family:     Volvo based SSDs
Device Model:     Volvo SSD 123 RUSTY 250GB
Serial Number:    1231232341234
LU WWN Device Id: 5 001234 a123f123
Firmware Version: XXX01234
User Capacity:    250,053,931,008 bytes [250 GB]
Sector Size:      512 bytes logical/physical
Rotation Rate:    Solid State Device
Form Factor:      2.5 inches
Device is:        In smartctl database [for details use: -P show]
ATA Version is:   ACS-2, ATA8-ACS T123/1234-X revision 123
SATA Version is:  SATA 3.1, 6.0 Gb/s (current: 6.0 Gb/s)
Local Time is:    Sat Nov 19 00:23:20 2016 CET
SMART support is: Available - device has SMART capability.
SMART support is: Enabled
"""

expected_results = {
    'serial': "1231232341234",
    'model': "Volvo SSD 123 RUSTY 250GB",
    'capacity': 250053931008,
    'form_factor': "2.5 inches",
    'is_ssd': True,
    'smart_well_known': True,
    'smart_available': True,
    'smart_enabled': True,
}
