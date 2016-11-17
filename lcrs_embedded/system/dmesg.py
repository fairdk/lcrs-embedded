import logging
import re

from lcrs_embedded.utils.validation import clean_int

from .. import models
from ..utils.decorators import run_command_with_timeout

logger = logging.getLogger(__name__)


@run_command_with_timeout("dmesg", mock_in_test=True)
def dmesg_analysis(scan_result, stdout, stderr, succeeded):
    """
    default_mock = True because dmesg output is different depending on Kernel.
    Ubuntu Kernel does not report logical blocks/hardware sectors.
    """

    if not succeeded:
        scan_result.dmesg = "{}\n{}".format(stderr, stdout)
        return

    scan_result.dmesg = stdout

    logger.info("called")
    """
    Find hard drives...
    """
    # This doesn't seem to work
    p = re.compile(r"\[(sd.)\].+(hardware sectors|logical blocks)", re.I)
    harddrives = []
    for line in stdout.split("\n"):
        m = p.search(line)
        if m:
            dev_name = "/dev/{}".format(m.group(1))
            harddrives.append(models.Harddrive(dev=dev_name))
            logger.info("Found disk drive {}".format(dev_name))

    scan_result.harddrives = harddrives

    ata_controllers = {}
    re_ata_controllers = re.compile(r"(ata\d)\:\s*(.+)")
    for line in stdout.split("\n"):
        m = re_ata_controllers.search(line)
        if m:
            ata_name = m.group(1)
            # Info is appended to...
            info = ata_controllers.get(ata_name, {'info': ''})['info']
            info = info + "\n" + m.group(2)
            ata_controllers[ata_name] = {'info': info,
                                         'pata': "PATA" in info,
                                         'sata': "SATA" in info}
            logger.info("Found ATA controller {}".format(ata_name))

    # Sort the keys because otherwise the output list will be inconsistent
    # and hard to test
    logger.debug(scan_result.disk_controllers)
    for k in sorted(ata_controllers.keys()):
        logger.info("Adding: {}".format(k))
        v = ata_controllers[k]
        scan_result.disk_controllers.append(
            models.DiskController(dev=k, sata=v['sata'], raw_info=v['info'])
        )

    # Matches "Memory: 485260K/523832K available"
    p = re.compile(r'Memory:\s\d+K/(\d+)K\savailable\s+\(', re.I)
    m = p.match(stdout)
    if m:
        scan_result.memory_total = clean_int(m.group(0))


dmesg_analysis.mock_output = """
[    0.000000] Linux version 4.7.2 (build@host) (gcc version 4.9.4 (Buildroot 2016.08.1) ) #9 SMP Fri Nov 11 19:02:44 CET 2016
[    0.000000] x86/fpu: xstate_offset[2]:  576, xstate_sizes[2]:  256
[    0.000000] x86/fpu: Supporting XSAVE feature 0x001: 'x87 floating point registers'
[    0.000000] x86/fpu: Supporting XSAVE feature 0x002: 'SSE registers'
[    0.000000] x86/fpu: Supporting XSAVE feature 0x004: 'AVX registers'
[    0.000000] x86/fpu: Enabled xstate features 0x7, context size is 832 bytes, using 'standard' format.
[    0.000000] x86/fpu: Using 'eager' FPU context switches.
[    0.000000] e820: BIOS-provided physical RAM map:
[    0.000000] BIOS-e820: [mem 0x0000000000000000-0x000000000009fbff] usable
[    0.000000] BIOS-e820: [mem 0x000000000009fc00-0x000000000009ffff] reserved
[    0.000000] BIOS-e820: [mem 0x00000000000f0000-0x00000000000fffff] reserved
[    0.000000] BIOS-e820: [mem 0x0000000000100000-0x000000001ffeffff] usable
[    0.000000] BIOS-e820: [mem 0x000000001fff0000-0x000000001fffffff] ACPI data
[    0.000000] BIOS-e820: [mem 0x00000000fffc0000-0x00000000ffffffff] reserved
[    0.000000] NX (Execute Disable) protection: active
[    0.000000] SMBIOS 2.5 present.
[    0.000000] DMI: innotek GmbH VirtualBox/VirtualBox, BIOS VirtualBox 12/01/2006
[    0.000000] e820: update [mem 0x00000000-0x00000fff] usable ==> reserved
[    0.000000] e820: remove [mem 0x000a0000-0x000fffff] usable
[    0.000000] e820: last_pfn = 0x1fff0 max_arch_pfn = 0x1000000
[    0.000000] MTRR default type: uncachable
[    0.000000] MTRR variable ranges disabled:
[    0.000000] MTRR: Disabled
[    0.000000] x86/PAT: MTRRs disabled, skipping PAT initialization too.
[    0.000000] x86/PAT: Configuration [0-7]: WB  WT  UC- UC  WB  WT  UC- UC
[    0.000000] CPU MTRRs all blank - virtualized system.
[    0.000000] found SMP MP-table at [mem 0x0009fff0-0x0009ffff] mapped at [c009fff0]
[    0.000000] Scanning 1 areas for low memory corruption
[    0.000000] initial memory mapped: [mem 0x00000000-0x035fffff]
[    0.000000] Base memory trampoline at [c009b000] 9b000 size 16384
[    0.000000] BRK [0x0311d000, 0x0311dfff] PGTABLE
[    0.000000] BRK [0x0311e000, 0x0311efff] PGTABLE
[    0.000000] ACPI: Early table checksum verification disabled
[    0.000000] ACPI: RSDP 0x00000000000E0000 000024 (v02 VBOX  )
[    0.000000] ACPI: XSDT 0x000000001FFF0030 00003C (v01 VBOX   VBOXXSDT 00000001 ASL  00000061)
[    0.000000] ACPI: FACP 0x000000001FFF00F0 0000F4 (v04 VBOX   VBOXFACP 00000001 ASL  00000061)
[    0.000000] ACPI: DSDT 0x000000001FFF0470 002118 (v01 VBOX   VBOXBIOS 00000002 INTL 20160108)
[    0.000000] ACPI: FACS 0x000000001FFF0200 000040
[    0.000000] ACPI: FACS 0x000000001FFF0200 000040
[    0.000000] ACPI: APIC 0x000000001FFF0240 000054 (v02 VBOX   VBOXAPIC 00000001 ASL  00000061)
[    0.000000] ACPI: SSDT 0x000000001FFF02A0 0001CC (v01 VBOX   VBOXCPUT 00000002 INTL 20160108)
[    0.000000] ACPI: Local APIC address 0xfee00000
[    0.000000] 0MB HIGHMEM available.
[    0.000000] 511MB LOWMEM available.
[    0.000000]   mapped low ram: 0 - 1fff0000
[    0.000000]   low ram: 0 - 1fff0000
[    0.000000] Zone ranges:
[    0.000000]   DMA      [mem 0x0000000000001000-0x0000000000ffffff]
[    0.000000]   Normal   [mem 0x0000000001000000-0x000000001ffeffff]
[    0.000000]   HighMem  empty
[    0.000000] Movable zone start for each node
[    0.000000] Early memory node ranges
[    0.000000]   node   0: [mem 0x0000000000001000-0x000000000009efff]
[    0.000000]   node   0: [mem 0x0000000000100000-0x000000001ffeffff]
[    0.000000] Initmem setup node 0 [mem 0x0000000000001000-0x000000001ffeffff]
[    0.000000] On node 0 totalpages: 130958
[    0.000000] free_area_init_node: node 0, pgdat c1f05d00, node_mem_map dfbf0020
[    0.000000]   DMA zone: 32 pages used for memmap
[    0.000000]   DMA zone: 0 pages reserved
[    0.000000]   DMA zone: 3998 pages, LIFO batch:0
[    0.000000]   Normal zone: 992 pages used for memmap
[    0.000000]   Normal zone: 126960 pages, LIFO batch:31
[    0.000000] Using APIC driver default
[    0.000000] ACPI: PM-Timer IO Port: 0x4008
[    0.000000] ACPI: Local APIC address 0xfee00000
[    0.000000] IOAPIC[0]: apic_id 1, version 17, address 0xfec00000, GSI 0-23
[    0.000000] ACPI: INT_SRC_OVR (bus 0 bus_irq 0 global_irq 2 dfl dfl)
[    0.000000] ACPI: INT_SRC_OVR (bus 0 bus_irq 9 global_irq 9 high level)
[    0.000000] ACPI: IRQ0 used by override.
[    0.000000] ACPI: IRQ9 used by override.
[    0.000000] Using ACPI (MADT) for SMP configuration information
[    0.000000] smpboot: Allowing 1 CPUs, 0 hotplug CPUs
[    0.000000] e820: [mem 0x20000000-0xfffbffff] available for PCI devices
[    0.000000] clocksource: refined-jiffies: mask: 0xffffffff max_cycles: 0xffffffff, max_idle_ns: 1910969940391419 ns
[    0.000000] setup_percpu: NR_CPUS:8 nr_cpumask_bits:8 nr_cpu_ids:1 nr_node_ids:1
[    0.000000] percpu: Embedded 17 pages/cpu @dfbdb000 s48780 r0 d20852 u69632
[    0.000000] pcpu-alloc: s48780 r0 d20852 u69632 alloc=17*4096
[    0.000000] pcpu-alloc: [0] 0
[    0.000000] Built 1 zonelists in Zone order, mobility grouping on.  Total pages: 129934
[    0.000000] Kernel command line: BOOT_IMAGE=/boot/bzImage root=/dev/sr0
[    0.000000] PID hash table entries: 2048 (order: 1, 8192 bytes)
[    0.000000] Dentry cache hash table entries: 65536 (order: 6, 262144 bytes)
[    0.000000] Inode-cache hash table entries: 32768 (order: 5, 131072 bytes)
[    0.000000] Initializing CPU#0
[    0.000000] Initializing HighMem for node 0 (00000000:00000000)
[    0.000000] Memory: 485260K/523832K available (10851K kernel code, 787K rwdata, 3824K rodata, 17648K init, 628K bss, 38572K reserved, 0K cma-reserved, 0K highmem)
[    0.000000] virtual kernel memory layout:
[    0.000000]     fixmap  : 0xfff16000 - 0xfffff000   ( 932 kB)
[    0.000000]     pkmap   : 0xffc00000 - 0xffe00000   (2048 kB)
[    0.000000]     vmalloc : 0xe07f0000 - 0xffbfe000   ( 500 MB)
[    0.000000]     lowmem  : 0xc0000000 - 0xdfff0000   ( 511 MB)
[    0.000000]       .init : 0xc1f1e000 - 0xc305a000   (17648 kB)
[    0.000000]       .data : 0xc1a99102 - 0xc1f1cc80   (4622 kB)
[    0.000000]       .text : 0xc1000000 - 0xc1a99102   (10852 kB)
[    0.000000] Checking if this processor honours the WP bit even in supervisor mode...Ok.
[    0.000000] SLUB: HWalign=64, Order=0-3, MinObjects=0, CPUs=1, Nodes=1
[    0.000000] Hierarchical RCU implementation.
[    0.000000]     Build-time adjustment of leaf fanout to 32.
[    0.000000]     RCU restricting CPUs from NR_CPUS=8 to nr_cpu_ids=1.
[    0.000000] RCU: Adjusting geometry for rcu_fanout_leaf=32, nr_cpu_ids=1
[    0.000000] NR_IRQS:2304 nr_irqs:256 16
[    0.000000] CPU 0 irqstacks, hard=df41a000 soft=df41c000
[    0.000000] Console: colour VGA+ 80x25
[    0.000000] console [tty0] enabled
[    0.000000] tsc: Fast TSC calibration failed
[    0.000000] tsc: Unable to calibrate against PIT
[    0.000000] tsc: using PMTIMER reference calibration
[    0.000000] tsc: Detected 2691.209 MHz processor
[    0.000066] Calibrating delay loop (skipped), value calculated using timer frequency.. 5382.41 BogoMIPS (lpj=2691209)
[    0.000906] pid_max: default: 32768 minimum: 301
[    0.001467] ACPI: Core revision 20160422
[    0.002522] ACPI: 2 ACPI AML tables successfully acquired and loaded
[    0.003886]
[    0.003931] Mount-cache hash table entries: 1024 (order: 0, 4096 bytes)
[    0.004486] Mountpoint-cache hash table entries: 1024 (order: 0, 4096 bytes)
[    0.005235] CPU: Physical Processor ID: 0
[    0.005973] mce: CPU supports 0 MCE banks
[    0.006476] process: using mwait in idle threads
[    0.007283] Last level iTLB entries: 4KB 512, 2MB 8, 4MB 8
[    0.007969] Last level dTLB entries: 4KB 512, 2MB 32, 4MB 32, 1GB 0
[    0.032404] Freeing SMP alternatives memory: 40K (c305a000 - c3064000)
[    0.033538] smpboot: Max logical packages: 1
[    0.034189] smpboot: APIC(0) Converting physical 0 to logical package 0
[    0.034807] Enabling APIC mode:  Flat.  Using 1 I/O APICs
[    0.036101] ..TIMER: vector=0x30 apic1=0 pin1=2 apic2=-1 pin2=-1
[    0.148506] smpboot: CPU0: Intel(R) Core(TM) i7-2620M CPU @ 2.70GHz (family: 0x6, model: 0x2a, stepping: 0x7)
[    0.149783] Performance Events: unsupported p6 CPU model 42 no PMU driver, software events only.
[    0.151591] x86: Booted up 1 node, 1 CPUs
[    0.152137] smpboot: Total of 1 processors activated (5382.41 BogoMIPS)
[    0.152767] devtmpfs: initialized
[    0.153567] clocksource: jiffies: mask: 0xffffffff max_cycles: 0xffffffff, max_idle_ns: 1911260446275000 ns
[    0.154569] NET: Registered protocol family 16
[    0.155123] cpuidle: using governor menu
[    0.155612] ACPI: bus type PCI registered
[    0.156377] PCI : PCI BIOS area is rw and x. Use pci=nobios if you want it NX.
[    0.157305] PCI: PCI BIOS revision 2.10 entry at 0xfda26, last bus=0
[    0.158084] PCI: Using configuration type 1 for base access
[    0.161689] kworker/u2:0 (27) used greatest stack depth: 7308 bytes left
[    0.162672] kworker/u2:0 (17) used greatest stack depth: 7088 bytes left
[    0.163349] kworker/u2:1 (71) used greatest stack depth: 6816 bytes left
[    0.171024] HugeTLB registered 2 MB page size, pre-allocated 0 pages
[    0.171897] ACPI: Added _OSI(Module Device)
[    0.172611] ACPI: Added _OSI(Processor Device)
[    0.173156] ACPI: Added _OSI(3.0 _SCP Extensions)
[    0.174182] ACPI: Added _OSI(Processor Aggregator Device)
[    0.174837] ACPI: Executed 1 blocks of module-level executable AML code
[    0.177379] ACPI: Interpreter enabled
[    0.178109] ACPI: (supports S0 S5)
[    0.178539] ACPI: Using IOAPIC for interrupt routing
[    0.179241] PCI: Using host bridge windows from ACPI; if necessary, use "pci=nocrs" and report a bug
[    0.183897] ACPI: PCI Root Bridge [PCI0] (domain 0000 [bus 00-ff])
[    0.184486] acpi PNP0A03:00: _OSC: OS supports [ASPM ClockPM Segments MSI]
[    0.185128] acpi PNP0A03:00: _OSC failed (AE_NOT_FOUND); disabling ASPM
[    0.185702] acpi PNP0A03:00: fail to add MMCONFIG information, can't access extended PCI configuration space under this bridge.
[    0.186642] PCI host bridge to bus 0000:00
[    0.187298] pci_bus 0000:00: root bus resource [io  0x0000-0x0cf7 window]
[    0.189560] pci_bus 0000:00: root bus resource [io  0x0d00-0xffff window]
[    0.190633] pci_bus 0000:00: root bus resource [mem 0x000a0000-0x000bffff window]
[    0.191727] pci_bus 0000:00: root bus resource [mem 0x20000000-0xffdfffff window]
[    0.193084] pci_bus 0000:00: root bus resource [bus 00-ff]
[    0.193623] pci 0000:00:00.0: [8086:1237] type 00 class 0x060000
[    0.194230] pci 0000:00:01.0: [8086:7000] type 00 class 0x060100
[    0.194770] pci 0000:00:01.1: [8086:7111] type 00 class 0x01018a
[    0.195052] pci 0000:00:01.1: reg 0x20: [io  0xd000-0xd00f]
[    0.195168] pci 0000:00:01.1: legacy IDE quirk: reg 0x10: [io  0x01f0-0x01f7]
[    0.195773] pci 0000:00:01.1: legacy IDE quirk: reg 0x14: [io  0x03f6]
[    0.196105] pci 0000:00:01.1: legacy IDE quirk: reg 0x18: [io  0x0170-0x0177]
[    0.197049] pci 0000:00:01.1: legacy IDE quirk: reg 0x1c: [io  0x0376]
[    0.198315] pci 0000:00:02.0: [80ee:beef] type 00 class 0x030000
[    0.198908] pci 0000:00:02.0: reg 0x10: [mem 0xe0000000-0xe0ffffff pref]
[    0.202573] pci 0000:00:03.0: [8086:100e] type 00 class 0x020000
[    0.202997] pci 0000:00:03.0: reg 0x10: [mem 0xf0000000-0xf001ffff]
[    0.203472] pci 0000:00:03.0: reg 0x18: [io  0xd010-0xd017]
[    0.204841] pci 0000:00:04.0: [80ee:cafe] type 00 class 0x088000
[    0.205138] pci 0000:00:04.0: reg 0x10: [io  0xd020-0xd03f]
[    0.205419] pci 0000:00:04.0: reg 0x14: [mem 0xf0400000-0xf07fffff]
[    0.205661] pci 0000:00:04.0: reg 0x18: [mem 0xf0800000-0xf0803fff pref]
[    0.206911] pci 0000:00:05.0: [8086:2415] type 00 class 0x040100
[    0.206977] pci 0000:00:05.0: reg 0x10: [io  0xd100-0xd1ff]
[    0.207024] pci 0000:00:05.0: reg 0x14: [io  0xd200-0xd23f]
[    0.207428] pci 0000:00:06.0: [106b:003f] type 00 class 0x0c0310
[    0.208268] pci 0000:00:06.0: reg 0x10: [mem 0xf0804000-0xf0804fff]
[    0.210371] pci 0000:00:07.0: [8086:7113] type 00 class 0x068000
[    0.211066] pci_bus 0000:00: on NUMA node 0
[    0.211762] ACPI: PCI Interrupt Link [LNKA] (IRQs 5 9 10 *11)
[    0.213256] ACPI: PCI Interrupt Link [LNKB] (IRQs 5 9 10 *11)
[    0.214645] ACPI: PCI Interrupt Link [LNKC] (IRQs 5 9 *10 11)
[    0.215758] ACPI: PCI Interrupt Link [LNKD] (IRQs 5 *9 10 11)
[    0.217530] ACPI: Enabled 2 GPEs in block 00 to 07
[    0.218399] vgaarb: setting as boot device: PCI:0000:00:02.0
[    0.218951] vgaarb: device added: PCI:0000:00:02.0,decodes=io+mem,owns=io+mem,locks=none
[    0.219412] vgaarb: loaded
[    0.220023] vgaarb: bridge control possible 0000:00:02.0
[    0.221170] SCSI subsystem initialized
[    0.221597] libata version 3.00 loaded.
[    0.221670] ACPI: bus type USB registered
[    0.222270] usbcore: registered new interface driver usbfs
[    0.222797] usbcore: registered new interface driver hub
[    0.223064] usbcore: registered new device driver usb
[    0.223608] pps_core: LinuxPPS API ver. 1 registered
[    0.224162] pps_core: Software ver. 5.3.6 - Copyright 2005-2007 Rodolfo Giometti <giometti@linux.it>
[    0.225578] PTP clock support registered
[    0.226350] PCI: Using ACPI for IRQ routing
[    0.226935] PCI: pci_cache_line_size set to 64 bytes
[    0.227283] e820: reserve RAM buffer [mem 0x0009fc00-0x0009ffff]
[    0.227299] e820: reserve RAM buffer [mem 0x1fff0000-0x1fffffff]
[    0.227658] amd_nb: Cannot enumerate AMD northbridges
[    0.228293] clocksource: Switched to clocksource refined-jiffies
[    0.232604] VFS: Disk quotas dquot_6.6.0
[    0.233451] VFS: Dquot-cache hash table entries: 1024 (order 0, 4096 bytes)
[    0.234570] pnp: PnP ACPI init
[    0.235067] pnp 00:00: Plug and Play ACPI device, IDs PNP0303 (active)
[    0.235142] pnp 00:01: Plug and Play ACPI device, IDs PNP0f03 (active)
[    0.236093] pnp: PnP ACPI: found 2 devices
[    0.273446] clocksource: acpi_pm: mask: 0xffffff max_cycles: 0xffffff, max_idle_ns: 2085701024 ns
[    0.283937] clocksource: Switched to clocksource acpi_pm
[    0.284577] pci_bus 0000:00: resource 4 [io  0x0000-0x0cf7 window]
[    0.284579] pci_bus 0000:00: resource 5 [io  0x0d00-0xffff window]
[    0.284580] pci_bus 0000:00: resource 6 [mem 0x000a0000-0x000bffff window]
[    0.284582] pci_bus 0000:00: resource 7 [mem 0x20000000-0xffdfffff window]
[    0.284603] NET: Registered protocol family 2
[    0.285202] TCP established hash table entries: 4096 (order: 2, 16384 bytes)
[    0.285875] TCP bind hash table entries: 4096 (order: 3, 32768 bytes)
[    0.286746] TCP: Hash tables configured (established 4096 bind 4096)
[    0.287579] UDP hash table entries: 256 (order: 1, 8192 bytes)
[    0.288021] UDP-Lite hash table entries: 256 (order: 1, 8192 bytes)
[    0.288644] NET: Registered protocol family 1
[    0.289145] RPC: Registered named UNIX socket transport module.
[    0.289608] RPC: Registered udp transport module.
[    0.290123] RPC: Registered tcp transport module.
[    0.290490] RPC: Registered tcp NFSv4.1 backchannel transport module.
[    0.291277] pci 0000:00:00.0: Limiting direct PCI/PCI transfers
[    0.292070] pci 0000:00:01.0: Activating ISA DMA hang workarounds
[    0.292725] pci 0000:00:02.0: Video device with shadowed ROM at [mem 0x000c0000-0x000dffff]
[    0.295482] PCI: CLS 0 bytes, default 64
[    0.391970] hrtimer: interrupt took 4144382 ns
[    0.546510] RAPL PMU: API unit is 2^-32 Joules, 3 fixed counters, 10737418240 ms ovfl timer
[    0.547597] RAPL PMU: hw unit of domain pp0-core 2^-0 Joules
[    0.548040] RAPL PMU: hw unit of domain package 2^-0 Joules
[    0.548607] RAPL PMU: hw unit of domain pp1-gpu 2^-0 Joules
[    0.549161] platform rtc_cmos: registered platform RTC device (no PNP device found)
[    0.550248] Scanning for low memory corruption every 60 seconds
[    0.551442] futex hash table entries: 256 (order: 2, 16384 bytes)
[    0.552864] audit: initializing netlink subsys (disabled)
[    0.553036] audit: type=2000 audit(1478887558.448:1): initialized
[    0.554001] workingset: timestamp_bits=28 max_order=17 bucket_order=0
[    0.560044] NFS: Registering the id_resolver key type
[    0.560630] Key type id_resolver registered
[    0.561142] Key type id_legacy registered
[    0.562384] Block layer SCSI generic (bsg) driver version 0.4 loaded (major 251)
[    0.563596] io scheduler noop registered
[    0.564021] io scheduler deadline registered
[    0.564641] io scheduler cfq registered (default)
[    0.565177] pci_hotplug: PCI Hot Plug PCI Core version: 0.5
[    0.565865] ACPI: AC Adapter [AC] (on-line)
[    0.566944] input: Power Button as /devices/LNXSYSTM:00/LNXPWRBN:00/input/input0
[    0.567997] ACPI: Power Button [PWRF]
[    0.568508] input: Sleep Button as /devices/LNXSYSTM:00/LNXSLPBN:00/input/input1
[    0.569482] ACPI: Sleep Button [SLPF]
[    0.569611] ACPI: Video Device [GFX0] (multi-head: yes  rom: no  post: no)
[    0.571001] input: Video Bus as /devices/LNXSYSTM:00/LNXSYBUS:00/PNP0A03:00/LNXVIDEO:00/input/input2
[    0.572425] Warning: Processor Platform Limit event detected, but not handled.
[    0.573436] Consider compiling CPUfreq support into your kernel.
[    0.574339] ACPI: Battery Slot [BAT0] (battery present)
[    0.575213] Serial: 8250/16550 driver, 4 ports, IRQ sharing enabled
[    0.576371] Non-volatile memory driver v1.3
[    0.577012] [drm] Initialized drm 1.1.0 20060810
[    0.579959] loop: module loaded
[    0.580619] ata_piix 0000:00:01.1: version 2.13
[    0.581224] scsi host0: ata_piix
[    0.581875] scsi host1: ata_piix
[    0.582466] ata1: PATA max UDMA/33 cmd 0x1f0 ctl 0x3f6 bmdma 0xd000 irq 14
[    0.583025] ata2: PATA max UDMA/33 cmd 0x170 ctl 0x376 bmdma 0xd008 irq 15
[    0.583745] libphy: Fixed MDIO Bus: probed
[    0.584637] pcnet32: pcnet32.c:v1.35 21.Apr.2008 tsbogend@alpha.franken.de
[    0.585729] Atheros(R) L2 Ethernet Driver - version 2.2.3
[    0.586020] Copyright (c) 2007 Atheros Corporation.
[    0.586647] cnic: QLogic cnicDriver v2.5.22 (July 20, 2015)
[    0.587585] bnx2x: QLogic 5771x/578xx 10/20-Gigabit Ethernet Driver bnx2x 1.712.30-0 (2014/02/10)
[    0.589057] bna: QLogic BR-series 10G Ethernet driver - version: 3.2.25.1
[    0.589741] enic: Cisco VIC Ethernet NIC Driver, ver 2.3.0.20
[    0.590317] dmfe: Davicom DM9xxx net driver, version 1.36.4 (2002-01-17)
[    0.592112] uli526x: ULi M5261/M5263 net driver, version 0.9.3 (2005-7-29)
[    0.593953] vxge: Copyright(c) 2002-2010 Exar Corp.
[    0.594975] vxge: Driver version: 2.5.3.22640-k
[    0.596071] e100: Intel(R) PRO/100 Network Driver, 3.5.24-k2-NAPI
[    0.597103] e100: Copyright(c) 1999-2006 Intel Corporation
[    0.598258] e1000: Intel(R) PRO/1000 Network Driver - version 7.3.21-k8-NAPI
[    0.599799] e1000: Copyright (c) 1999-2006 Intel Corporation.
[    0.736454] ata1.00: ATA-6: VBOX HARDDISK, 1.0, max UDMA/133
[    0.737006] ata1.00: 17573 sectors, multi 128: LBA
[    0.737557] ata1.01: ATAPI: VBOX CD-ROM, 1.0, max UDMA/133
[    0.738350] ata1.00: configured for UDMA/33
[    0.739794] ata1.01: configured for UDMA/33
[    0.744637] scsi 0:0:0:0: Direct-Access     ATA      VBOX HARDDISK    1.0  PQ: 0 ANSI: 5
[    0.746138] sd 0:0:0:0: [sda] 17573 512-byte logical blocks: (9.00 MB/8.58 MiB)
[    0.747093] sd 0:0:0:0: [sda] Write Protect is off
[    0.747699] sd 0:0:0:0: [sda] Mode Sense: 00 3a 00 00
[    0.747727] sd 0:0:0:0: [sda] Write cache: enabled, read cache: enabled, doesn't support DPO or FUA
[    0.749021] sd 0:0:0:0: Attached scsi generic sg0 type 0
[    0.755796] scsi 0:0:1:0: CD-ROM            VBOX     CD-ROM           1.0  PQ: 0 ANSI: 5
[    0.757330] sd 0:0:0:0: [sda] Attached SCSI disk
[    0.758468] sr 0:0:1:0: [sr0] scsi3-mmc drive: 32x/32x xa/form2 tray
[    0.759054] cdrom: Uniform CD-ROM driver Revision: 3.20
[    0.759781] sr 0:0:1:0: Attached scsi CD-ROM sr0
[    0.759944] sr 0:0:1:0: Attached scsi generic sg1 type 5
[    0.957074] e1000 0000:00:03.0 eth0: (PCI:33MHz:32-bit) 08:00:27:8b:cb:f2
[    0.957801] e1000 0000:00:03.0 eth0: Intel(R) PRO/1000 Network Connection
[    0.958970] e1000e: Intel(R) PRO/1000 Network Driver - 3.2.6-k
[    0.959817] e1000e: Copyright(c) 1999 - 2015 Intel Corporation.
[    0.960472] igb: Intel(R) Gigabit Ethernet Network Driver - version 5.3.0-k
[    0.960772] igb: Copyright (c) 2007-2014 Intel Corporation.
[    0.962043] igbvf: Intel(R) Gigabit Virtual Function Network Driver - version 2.0.2-k
[    0.963256] igbvf: Copyright (c) 2009 - 2012 Intel Corporation.
[    0.963909] ixgbe: Intel(R) 10 Gigabit PCI Express Network Driver - version 4.4.0-k
[    0.965064] ixgbe: Copyright (c) 1999-2016 Intel Corporation.
[    0.965775] ixgbevf: Intel(R) 10 Gigabit PCI Express Virtual Function Network Driver - version 2.12.1-k
[    0.967187] ixgbevf: Copyright (c) 2009 - 2015 Intel Corporation.
[    0.968055] i40e: Intel(R) Ethernet Connection XL710 Network Driver - version 1.5.16-k
[    0.969070] i40e: Copyright (c) 2013 - 2014 Intel Corporation.
[    0.969638] ixgb: Intel(R) PRO/10GbE Network Driver - version 1.0.135-k2-NAPI
[    0.970276] ixgb: Copyright (c) 1999-2008 Intel Corporation.
[    0.970585] i40evf: Intel(R) 40-10 Gigabit Virtual Function Network Driver - version 1.5.10-k
[    0.971979] Copyright (c) 2013 - 2015 Intel Corporation.
[    0.972670] Intel(R) Ethernet Switch Host Interface Driver - version 0.19.3-k
[    0.973496] Copyright (c) 2013 - 2016 Intel Corporation.
[    0.974138] sky2: driver version 1.30
[    0.974804] myri10ge: Version 1.5.3-1.534
[    0.975324] ns83820.c: National Semiconductor DP83820 10/100/1000 driver.
[    0.975712] nfp_netvf: NFP VF Network driver, Copyright (C) 2014-2015 Netronome Systems
[    0.977050] pch_gbe: EG20T PCH Gigabit Ethernet Driver - version 1.01
[    0.977807] QLogic 1/10 GbE Converged/Intelligent Ethernet Driver v5.3.64
[    0.979094] QLogic/NetXen Network Driver v4.0.82
[    0.979807] qed_init called
[    0.980466] QLogic FastLinQ 4xxxx Core Module qed 8.7.1.20
[    0.981296] Solarflare NET driver v4.0
[    0.982376] usbcore: registered new interface driver catc
[    0.983089] usbcore: registered new interface driver kaweth
[    0.983679] pegasus: v0.9.3 (2013/04/25), Pegasus/Pegasus II USB Ethernet driver
[    0.985111] usbcore: registered new interface driver pegasus
[    0.985722] usbcore: registered new interface driver rtl8150
[    0.986298] usbcore: registered new interface driver r8152
[    0.986574] hso: drivers/net/usb/hso.c: Option Wireless
[    0.987106] usbcore: registered new interface driver hso
[    0.987780] usbcore: registered new interface driver lan78xx
[    0.989004] usbcore: registered new interface driver asix
[    0.989626] usbcore: registered new interface driver ax88179_178a
[    0.990188] usbcore: registered new interface driver cdc_ether
[    0.990610] usbcore: registered new interface driver net1080
[    0.991156] usbcore: registered new interface driver cdc_subset
[    0.991640] usbcore: registered new interface driver zaurus
[    0.992808] usbcore: registered new interface driver ipheth
[    0.993087] usbcore: registered new interface driver cdc_ncm
[    0.993909] ehci_hcd: USB 2.0 'Enhanced' Host Controller (EHCI) Driver
[    0.994617] ehci-pci: EHCI PCI platform driver
[    0.995141] ohci_hcd: USB 1.1 'Open' Host Controller (OHCI) Driver
[    0.995900] ohci-pci: OHCI PCI platform driver
[    0.997193] ohci-pci 0000:00:06.0: OHCI PCI host controller
[    0.997850] ohci-pci 0000:00:06.0: new USB bus registered, assigned bus number 1
[    0.999491] ohci-pci 0000:00:06.0: irq 22, io mem 0xf0804000
[    1.051843] usb usb1: New USB device found, idVendor=1d6b, idProduct=0001
[    1.052562] usb usb1: New USB device strings: Mfr=3, Product=2, SerialNumber=1
[    1.054995] usb usb1: Product: OHCI PCI host controller
[    1.055786] usb usb1: Manufacturer: Linux 4.7.2 ohci_hcd
[    1.056516] usb usb1: SerialNumber: 0000:00:06.0
[    1.056925] hub 1-0:1.0: USB hub found
[    1.057763] hub 1-0:1.0: 12 ports detected
[    1.059344] uhci_hcd: USB Universal Host Controller Interface driver
[    1.060532] usbcore: registered new interface driver usblp
[    1.061902] usbcore: registered new interface driver usb-storage
[    1.062896] i8042: PNP: PS/2 Controller [PNP0303:PS2K,PNP0f03:PS2M] at 0x60,0x64 irq 1,12
[    1.064954] serio: i8042 KBD port at 0x60,0x64 irq 1
[    1.065734] serio: i8042 AUX port at 0x60,0x64 irq 12
[    1.066372] mousedev: PS/2 mouse device common for all mice
[    1.067514] input: AT Translated Set 2 keyboard as /devices/platform/i8042/serio0/input/input3
[    1.069564] rtc_cmos rtc_cmos: rtc core: registered rtc_cmos as rtc0
[    1.071058] rtc_cmos rtc_cmos: alarms up to one day, 114 bytes nvram
[    1.071952] hidraw: raw HID events driver (C) Jiri Kosina
[    1.084096] usbcore: registered new interface driver usbhid
[    1.084803] usbhid: USB HID core driver
[    1.085362] Netfilter messages via NETLINK v0.30.
[    1.086217] nf_conntrack version 0.5.0 (8192 buckets, 32768 max)
[    1.087053] ctnetlink v0.93: registering with nfnetlink.
[    1.087983] ip_tables: (C) 2000-2006 Netfilter Core Team
[    1.088773] Initializing XFRM netlink socket
[    1.090323] NET: Registered protocol family 10
[    1.091336] ip6_tables: (C) 2000-2006 Netfilter Core Team
[    1.092490] sit: IPv6 over IPv4 tunneling driver
[    1.093240] NET: Registered protocol family 17
[    1.093868] Key type dns_resolver registered
[    1.095283] microcode: CPU0 sig=0x206a7, pf=0x10, revision=0x0
[    1.096004] microcode: Microcode Update Driver: v2.01 <tigran@aivazian.fsnet.co.uk>, Peter Oruba
[    1.097182] Using IPI No-Shortcut mode
[    1.097822] registered taskstats version 1
[    1.099058] console [netcon0] enabled
[    1.099674] netconsole: network logging started
[    1.103229] Freeing unused kernel memory: 17648K (c1f1e000 - c305a000)
[    1.105417] Write protecting the kernel text: 10856k
[    1.106077] Write protecting the kernel read-only data: 3832k
[    1.106723] NX-protecting the kernel data: 23960k
[    1.109054] mount (1111) used greatest stack depth: 6684 bytes left
[    1.182911] random: dd: uninitialized urandom read (512 bytes read, 13 bits of entropy available)
[    1.188883] IPv6: ADDRCONF(NETDEV_UP): eth0: link is not ready
[    1.190273] e1000: eth0 NIC Link is Up 1000 Mbps Full Duplex, Flow Control: RX
[    1.192698] IPv6: ADDRCONF(NETDEV_CHANGE): eth0: link becomes ready
[    1.213762] netplugd (1141) used greatest stack depth: 6668 bytes left
[    1.220514] ip (1174) used greatest stack depth: 6612 bytes left
[    1.226354] random: mktemp: uninitialized urandom read (6 bytes read, 14 bits of entropy available)
[    1.233308] random: mktemp: uninitialized urandom read (6 bytes read, 14 bits of entropy available)
[    1.240464] random: mktemp: uninitialized urandom read (6 bytes read, 14 bits of entropy available)
[    1.246061] udhcpc (1181) used greatest stack depth: 6476 bytes left
[    1.248106] random: mktemp: uninitialized urandom read (6 bytes read, 14 bits of entropy available)
[    1.256102] random: dropbear: uninitialized urandom read (32 bytes read, 14 bits of entropy available)
[    1.432102] usb 1-1: new full-speed USB device number 2 using ohci-pci
[    1.551050] tsc: Refined TSC clocksource calibration: 2690.895 MHz
[    1.551694] clocksource: tsc: mask: 0xffffffffffffffff max_cycles: 0x26c9a56beaf, max_idle_ns: 440795343825 ns
[    1.648394] usb 1-1: New USB device found, idVendor=80ee, idProduct=0021
[    1.649123] usb 1-1: New USB device strings: Mfr=1, Product=3, SerialNumber=0
[    1.649849] usb 1-1: Product: USB Tablet
[    1.651117] usb 1-1: Manufacturer: VirtualBox
[    1.667161] input: VirtualBox USB Tablet as /devices/pci0000:00/0000:00:06.0/usb1/1-1/1-1:1.0/0003:80EE:0021.0001/input/input5
[    1.668497] hid-generic 0003:80EE:0021.0001: input,hidraw0: USB HID v1.10 Mouse [VirtualBox USB Tablet] on usb-0000:00:06.0-1/input0
[    2.553131] clocksource: Switched to clocksource tsc
[   27.426498] random: nonblocking pool is initialized
"""  # noqa

dmesg_analysis.expected_results = {
    'harddrives': [models.Harddrive(dev="/dev/sda")],
    'disk_controllers': [
        models.DiskController(
            dev='ata1',
            sata=False,
            raw_info=(
                '\nPATA max UDMA/33 cmd 0x1f0 ctl 0x3f6 bmdma 0xd000 irq 14'
            )
        ),
        models.DiskController(
            dev='ata2',
            sata=False,
            raw_info=(
                '\nPATA max UDMA/33 cmd 0x170 ctl 0x376 bmdma 0xd008 irq 15'
            )
        ),
    ],
}
