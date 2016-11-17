"""
Functions that read virtual files in /proc
"""
import logging
import re

from lcrs_embedded.utils.validation import clean_int_boolean

from ..utils.decorators import readfile

logger = logging.getLogger(__name__)


def __fetch_rows(scan_result, stdout, row_map, type_map=None):
    """
    Routine for fetching stuff
    """

    if not type_map:
        type_map = {}

    for row, attr in row_map.items():
        p = re.compile(r"^{row}:\s*(.+)\s*$".format(row=row), re.I | re.M)
        m = p.search(stdout)
        if m:
            match = m.group(1)
            logger.debug("Found DMI information for {}: {}".format(row, match))
            setattr(scan_result, attr, match)

    for attr, func in type_map.items():
        if scan_result[attr]:
            scan_result[attr] = func(scan_result[attr])


@readfile("/proc/cpuinfo", mock_in_test=True)
def cpuinfo(scan_result, file_contents, readable):
    """
    Reads memory information, but only in case DMI data collection has not
    produced a reliable memory_total.
    """

    if not readable:
        logger.critical("Couldn't read /proc/cpuinfo")
        return

    for line in file_contents.split("\n"):
        if line.startswith("model name"):
            model_name = line.split(":")[-1].strip()
            scan_result.processor_model_name = model_name


cpuinfo.mock_output = """
processor       : 0
vendor_id       : GenuineIntel
cpu family      : 6
model           : 42
model name      : Intel(R) Core(TM) i7-2620M CPU @ 2.70GHz
stepping        : 7
microcode       : 0x29
cpu MHz         : 1162.265
cache size      : 4096 KB
physical id     : 0
siblings        : 4
core id         : 0
cpu cores       : 2
apicid          : 0
initial apicid  : 0
fpu             : yes
fpu_exception   : yes
cpuid level     : 13
wp              : yes
flags           : fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx rdtscp lm constant_tsc arch_perfmon pebs bts nopl xtopology nonstop_tsc aperfmperf eagerfpu pni pclmulqdq dtes64 monitor ds_cpl vmx smx est tm2 ssse3 cx16 xtpr pdcm pcid sse4_1 sse4_2 x2apic popcnt tsc_deadline_timer aes xsave avx lahf_lm epb tpr_shadow vnmi flexpriority ept vpid xsaveopt dtherm ida arat pln pts
bugs            :
bogomips        : 5382.71
clflush size    : 64
cache_alignment : 64
address sizes   : 36 bits physical, 48 bits virtual
power management:

processor       : 1
vendor_id       : GenuineIntel
cpu family      : 6
model           : 42
model name      : Intel(R) Core(TM) i7-2620M CPU @ 2.70GHz
stepping        : 7
microcode       : 0x29
cpu MHz         : 1337.660
cache size      : 4096 KB
physical id     : 0
siblings        : 4
core id         : 0
cpu cores       : 2
apicid          : 1
initial apicid  : 1
fpu             : yes
fpu_exception   : yes
cpuid level     : 13
wp              : yes
flags           : fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx rdtscp lm constant_tsc arch_perfmon pebs bts nopl xtopology nonstop_tsc aperfmperf eagerfpu pni pclmulqdq dtes64 monitor ds_cpl vmx smx est tm2 ssse3 cx16 xtpr pdcm pcid sse4_1 sse4_2 x2apic popcnt tsc_deadline_timer aes xsave avx lahf_lm epb tpr_shadow vnmi flexpriority ept vpid xsaveopt dtherm ida arat pln pts
bugs            :
bogomips        : 5382.71
clflush size    : 64
cache_alignment : 64
address sizes   : 36 bits physical, 48 bits virtual
power management:

processor       : 2
vendor_id       : GenuineIntel
cpu family      : 6
model           : 42
model name      : Intel(R) Core(TM) i7-2620M CPU @ 2.70GHz
stepping        : 7
microcode       : 0x29
cpu MHz         : 1054.371
cache size      : 4096 KB
physical id     : 0
siblings        : 4
core id         : 1
cpu cores       : 2
apicid          : 2
initial apicid  : 2
fpu             : yes
fpu_exception   : yes
cpuid level     : 13
wp              : yes
flags           : fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx rdtscp lm constant_tsc arch_perfmon pebs bts nopl xtopology nonstop_tsc aperfmperf eagerfpu pni pclmulqdq dtes64 monitor ds_cpl vmx smx est tm2 ssse3 cx16 xtpr pdcm pcid sse4_1 sse4_2 x2apic popcnt tsc_deadline_timer aes xsave avx lahf_lm epb tpr_shadow vnmi flexpriority ept vpid xsaveopt dtherm ida arat pln pts
bugs            :
bogomips        : 5382.71
clflush size    : 64
cache_alignment : 64
address sizes   : 36 bits physical, 48 bits virtual
power management:

processor       : 3
vendor_id       : GenuineIntel
cpu family      : 6
model           : 42
model name      : Intel(R) Core(TM) i7-2620M CPU @ 2.70GHz
stepping        : 7
microcode       : 0x29
cpu MHz         : 992.144
cache size      : 4096 KB
physical id     : 0
siblings        : 4
core id         : 1
cpu cores       : 2
apicid          : 3
initial apicid  : 3
fpu             : yes
fpu_exception   : yes
cpuid level     : 13
wp              : yes
flags           : fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx rdtscp lm constant_tsc arch_perfmon pebs bts nopl xtopology nonstop_tsc aperfmperf eagerfpu pni pclmulqdq dtes64 monitor ds_cpl vmx smx est tm2 ssse3 cx16 xtpr pdcm pcid sse4_1 sse4_2 x2apic popcnt tsc_deadline_timer aes xsave avx lahf_lm epb tpr_shadow vnmi flexpriority ept vpid xsaveopt dtherm ida arat pln pts
bugs            :
bogomips        : 5382.71
clflush size    : 64
cache_alignment : 64
address sizes   : 36 bits physical, 48 bits virtual
power management:
"""  # noqa
cpuinfo.expected_results = {
    'processor_model_name': "Intel(R) Core(TM) i7-2620M CPU @ 2.70GHz",
}


@readfile("/proc/sys/dev/cdrom/info", mock_in_test=True)
def cdrominfo(scan_result, file_contents, readable):
    """
    Reads memory information, but only in case DMI data collection has not
    produced a reliable memory_total.
    """

    if not readable:
        logger.critical("Couldn't read /proc/sys/dev/cdrom/info")
        return

    # Key: DMI table column name
    # Value: ScanResult attribute
    row_map = {
        'drive name': 'cdrom_drive_name',
        'Can read DVD': 'cdrom_dvd',
        'Can write CD-R': 'cdrom_cdr',
        'Can write DVD-R': 'cdrom_dvdr',
    }
    type_map = {
        'cdrom_dvd': clean_int_boolean,
        'cdrom_dvdr': clean_int_boolean,
        'cdrom_cdr': clean_int_boolean,
    }
    __fetch_rows(scan_result, file_contents, row_map, type_map=type_map)

    scan_result.cdrom = bool(scan_result.cdrom_drive_name)


cdrominfo.mock_output = """
CD-ROM information, Id: cdrom.c 3.20 2003/12/17

drive name:        sr0
drive speed:        32
drive # of slots:    1
Can close tray:        1
Can open tray:        1
Can lock tray:        1
Can change speed:    1
Can select disk:    0
Can read multisession:    1
Can read MCN:        1
Reports media changed:    1
Can play audio:        1
Can write CD-R:        0
Can write CD-RW:    0
Can read DVD:        1
Can write DVD-R:    0
Can write DVD-RAM:    0
Can read MRW:        1
Can write MRW:        1
Can write RAM:        1
"""
cdrominfo.expected_results = {
    'cdrom': True,
    'cdrom_drive_name': "sr0",
    'cdrom_dvd': True,
    'cdrom_dvdr': False,
    'cdrom_cdr': False,
}
