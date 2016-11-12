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

# from .. import models
from ..utils.decorators import run_command_with_timeout

logger = logging.getLogger(__name__)


@run_command_with_timeout("dmidecode -t system", mock_in_test=True)
def dmidecode_system(scan_result, stdout, stderr, succeeded):
    """
    default_mock = True because dmidecode needs root privileges
    Ubuntu Kernel does not report logical blocks/hardware sectors.
    """

    if not succeeded:
        return

    # Key: DMI table column name
    # Value: ScanResult attribute
    rows = {
        'Manufacturer': 'system_manufacturer',
        'Product Name': 'system_product_id',
        'Version': 'system_version',
        'UUID': 'system_uuid',
        'Serial Number': 'system_serial_number',
        'Family': 'system_family',
    }

    for row, attr in rows.items():
        p = re.compile(r"^\s+{row}:\s*(.+)\s*$".format(row=row), re.I | re.M)
        m = p.search(stdout)
        if m:
            match = m.group(1)
            logger.debug("Found DMI information for {}: {}".format(row, match))
            setattr(scan_result, attr, match)

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
