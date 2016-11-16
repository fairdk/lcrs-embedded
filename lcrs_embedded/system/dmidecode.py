"""
Analysis of the DMI table requires root access, therefore all tests are always
mocked.

From the dmidecode man page:

dmidecode  is a tool for dumping a computer's DMI (some say SMBIOS) table
contents in a human-readable format. This table contains a description of the
system's hardware components, as well as other useful pieces of information
such as serial numbers and BIOS revision. Thanks to this table, you can
retrieve this information without having to probe for the actual hardware.
While this is a good point in terms of report speed and safeness, this also
makes the presented information possibly unreliable.
"""

import logging
import re

from .. import models
from ..utils.decorators import run_command_with_timeout

logger = logging.getLogger(__name__)


def fetch_rows(scan_result, stdout, row_map, type_map=None):
    """
    Reused routine for fetching stuff from dmidecode -t <type> output
    """

    if not type_map:
        type_map = {}

    for row, attr in row_map.items():
        p = re.compile(r"^\s+{row}:\s*(.+)\s*$".format(row=row), re.I | re.M)
        m = p.search(stdout)
        if m:
            match = m.group(1)
            logger.debug("Found DMI information for {}: {}".format(row, match))
            setattr(scan_result, attr, match)

    for attr, func in type_map.items():
        if scan_result[attr]:
            scan_result[attr] = func(scan_result[attr])


def clean_int(str_value):
    numbers = [int(s) for s in str_value.split() if s.isdigit()]
    if len(numbers) == 0:
        return None
    if len(numbers) == 1:
        return numbers[0]
    raise TypeError("Several numbers in result")


@run_command_with_timeout("dmidecode -t system", mock_in_test=True)
def dmidecode_system(scan_result, stdout, stderr, succeeded):
    """
    default_mock = True because dmidecode needs root privileges
    """

    if not succeeded:
        return

    # Key: DMI table column name
    # Value: ScanResult attribute
    row_map = {
        'Manufacturer': 'system_manufacturer',
        'Product Name': 'system_product_id',
        'Version': 'system_version',
        'UUID': 'system_uuid',
        'Serial Number': 'system_serial_number',
        'Family': 'system_family',
    }
    fetch_rows(scan_result, stdout, row_map)


dmidecode_system.mock_output = """
# dmidecode 2.9
SMBIOS 2.4 present.

Handle 0x0001, DMI type 1, 27 bytes
System Information
        Manufacturer: LENOVO
        Product Name: 1952W5R
        Version: ThinkPad T60
        Serial Number: 01234566
        UUID: 01234567-1234-1234-1234-123456789ABC
        Wake-up Type: Power Switch
        SKU Number: Not Specified
        Family: ThinkPad T60
"""
dmidecode_system.expected_results = {
    'system_manufacturer': "LENOVO",
    'system_product_id': "1952W5R",
    'system_version': "ThinkPad T60",
    'system_uuid': "01234567-1234-1234-1234-123456789ABC",
    'system_serial_number': "01234566",
    'system_family': "ThinkPad T60",
}


@run_command_with_timeout("dmidecode -t baseboard", mock_in_test=True)
def dmidecode_baseboard(scan_result, stdout, stderr, succeeded):
    """
    default_mock = True because dmidecode needs root privileges
    """

    if not succeeded:
        return

    # Key: DMI table column name
    # Value: ScanResult attribute
    row_map = {
        'Manufacturer': 'baseboard_manufacturer',
        'Serial Number': 'baseboard_serial_number',
    }

    fetch_rows(scan_result, stdout, row_map)

dmidecode_baseboard.mock_output = """
# dmidecode 3.0
Getting SMBIOS data from sysfs.
SMBIOS 2.6 present.

Handle 0x000F, DMI type 2, 15 bytes
Base Board Information
    Manufacturer: LENOVO
    Product Name: OVONEL
    Version: Not Available
    Serial Number: 12345678
    Asset Tag: Not Available
    Features:
        Board is a hosting board
        Board is replaceable
    Location In Chassis: Not Available
    Chassis Handle: 0x0000
    Type: Motherboard
    Contained Object Handles: 0

Handle 0x0029, DMI type 10, 6 bytes
On Board Device Information
    Type: Other
    Status: Disabled
    Description: IBM Embedded Security hardware
"""
dmidecode_baseboard.expected_results = {
    'baseboard_manufacturer': "LENOVO",
    'baseboard_serial_number': "12345678",
}


@run_command_with_timeout("dmidecode -t chassis", mock_in_test=True)
def dmidecode_chassis(scan_result, stdout, stderr, succeeded):
    """
    default_mock = True because dmidecode needs root privileges
    """

    if not succeeded:
        return

    # Key: DMI table column name
    # Value: ScanResult attribute
    row_map = {
        'Manufacturer': 'chassis_manufacturer',
        'Type': 'chassis_type',
        'Serial Number': 'chassis_serial_number',
    }

    fetch_rows(scan_result, stdout, row_map)

dmidecode_chassis.mock_output = """
# dmidecode 3.0
Getting SMBIOS data from sysfs.
SMBIOS 2.6 present.

Handle 0x0010, DMI type 3, 21 bytes
Chassis Information
    Manufacturer: LENOVO
    Type: Notebook
    Lock: Not Present
    Version: Not Available
    Serial Number: X123YZ
    Asset Tag: No Asset Information
    Boot-up State: Unknown
    Power Supply State: Unknown
    Thermal State: Unknown
    Security Status: Unknown
    OEM Information: 0x00000000
    Height: Unspecified
    Number Of Power Cords: Unspecified
    Contained Elements: 0
"""
dmidecode_chassis.expected_results = {
    'chassis_manufacturer': "LENOVO",
    'chassis_type': "Notebook",
    'chassis_serial_number': "X123YZ",
}


@run_command_with_timeout("dmidecode -t memory", mock_in_test=True)
def dmidecode_memory(scan_result, stdout, stderr, succeeded):
    """
    default_mock = True because dmidecode needs root privileges
    """

    if not succeeded:
        return

    p = re.compile(r"^Memory\sDevice\n(?:[\s]{4}.+\n)+", re.I | re.M)

    for match in re.findall(p, stdout):
        memory_device = models.MemoryDevice()
        # Key: DMI table column name
        # Value: ScanResult attribute
        row_map = {
            'Size': 'capacity_mb',
            'Form Factor': 'form_factor',
            'Type': 'type_technology',
            'Speed': 'speed_mhz',
            'Locator': 'locator',
            'Bank Locator': 'locator_bank',
            'Data Width': 'data_bits',
            'Manufacturer': 'manufacturer',
        }
        type_map = {
            'capacity_mb': clean_int,
            'speed_mhz': clean_int,
            'data_bits': clean_int,
        }
        fetch_rows(memory_device, match, row_map, type_map=type_map)
        scan_result.memory_devices.append(memory_device)

    scan_result.memory_total = sum(
        [d.capacity_mb for d in scan_result.memory_devices]
    )
    scan_result.memory_devices_count = len(scan_result.memory_devices)


dmidecode_memory.mock_output = """
# dmidecode 3.0
Getting SMBIOS data from sysfs.
SMBIOS 2.6 present.

Handle 0x0005, DMI type 16, 15 bytes
Physical Memory Array
    Location: System Board Or Motherboard
    Use: System Memory
    Error Correction Type: None
    Maximum Capacity: 16 GB
    Error Information Handle: Not Provided
    Number Of Devices: 2

Handle 0x0006, DMI type 17, 28 bytes
Memory Device
    Array Handle: 0x0005
    Error Information Handle: Not Provided
    Total Width: 64 bits
    Data Width: 64 bits
    Size: 4096 MB
    Form Factor: SODIMM
    Set: None
    Locator: ChannelA-DIMM0
    Bank Locator: BANK 0
    Type: DDR3
    Type Detail: Synchronous
    Speed: 1333 MHz
    Manufacturer: Samsung
    Serial Number: 1234567
    Asset Tag: 12345678910
    Part Number: XYSADKLJADSL-132
    Rank: Unknown

Handle 0x0007, DMI type 17, 28 bytes
Memory Device
    Array Handle: 0x0005
    Error Information Handle: Not Provided
    Total Width: 64 bits
    Data Width: 64 bits
    Size: 4096 MB
    Form Factor: SODIMM
    Set: None
    Locator: ChannelB-DIMM0
    Bank Locator: BANK 2
    Type: DDR3
    Type Detail: Synchronous
    Speed: 1333 MHz
    Manufacturer: Samsung
    Serial Number: 1234567
    Asset Tag: 12345678910
    Part Number: XYSADKLJADSL-132
    Rank: Unknown
"""
dmidecode_memory.expected_results = {
    'memory_total': 8192,
    'memory_devices_count': 2,
    'memory_devices': [
        models.MemoryDevice(
            capacity_mb=4096,
            form_factor="SODIMM",
            type_technology="DDR3",
            speed_mhz=1333,
            locator="ChannelA-DIMM0",
            locator_bank="BANK 0",
            data_bits=64,
            manufacturer="Samsung",
        ),
        models.MemoryDevice(
            capacity_mb=4096,
            form_factor="SODIMM",
            type_technology="DDR3",
            speed_mhz=1333,
            locator="ChannelB-DIMM0",
            locator_bank="BANK 2",
            data_bits=64,
            manufacturer="Samsung",
        ),
    ],
}
