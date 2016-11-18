"""
Models in the protocol
======================

The protocol itself is embedded in JSON requests transmitted through an HTTP
server.

All classes in this module are fully serializable back and forth.

These are the states of an embedded server and can be observed by the
requesting attendant client.

"""
from .utils.models import JSONModel


class Command(JSONModel):

    #: Any member of protocol.COMMANDS
    command_id = None

    #: Dictionary of arguments for the command
    kwargs = {}


class Response(JSONModel):
    pass


class JobResponse(Response):

    #: A number denoting the job
    job_id = None


class StateResponse(Response):

    #: Something from STATES
    state_id = None


class ScanResult(Response):
    """
    Overall assumption: To simplify our understanding of hardware data found by
    our probing, we have to accept that data are not guaranteed to be found.

    All fields in our models are therefore nullable.

    YAGNI mentality: Try to make stuff that's simple, dump advanced stuff into
    raw output and improve the protocol in the future.

    Because the UI and the embedded server are usually bundled, we don't need
    to worry about things breaking in this interface.
    """

    processor_mhz = None
    processor_family = None
    processor_manufacturer = None
    processor_cores = None
    #: Raw, unparsed model name from cpuinfo
    processor_model_name = None

    battery = None

    harddrives = []
    screen = {}

    #: CD-ROM info from /proc
    cdrom = False
    cdrom_dvd = False
    cdrom_dvdr = False
    cdrom_cdr = False
    #: Necessary to eject the drive
    cdrom_drive_name = None
    #: Stores state that cdrom was ejected
    cdrom_ejected = False

    #: String information about ethernet NIC
    ethernet = None
    #: String information about WIFI interface
    wifi = None
    is_laptop = False
    #: Total amount of memory installed
    memory_total = None
    #: Memory devices = RAM blocks
    memory_devices_count = None
    #: Details of each memory device, may not be present or may defer from the
    #: count depending on how well dmi decode analysis performs
    memory_devices = []
    #: String information about graphics controller
    graphics_controller = None
    #: String information about USB controller
    usb_controller = None
    #: Boolean USB present
    has_usb = False
    #: List of disk controllers
    disk_controllers = []
    #: The perceived manufacturer of the whole computer system, e.g. Dell
    system_manufacturer = None
    #: Manufacturer system UUID (NOT the serial)
    system_uuid = None
    #: Manufacturer Product Name/ID (like P/N)
    system_product_id = None
    #: Manufacturer system version (normally the nice name like "Thinkpad T60")
    system_version = None
    #: Manufacturer system UUID (NOT the serial)
    system_uuid = None
    #: Manufacturer system serial number, other alternatives exist for ID'ing
    #: the chassis
    system_serial_number = None
    #: Manufacturer system family (normally the nice name like "Thinkpad T60")
    system_family = None
    #: Board manufacturer, often actually the brand / system_manufacturer
    baseboard_manufacturer = None
    #: Board system serial number, other alternatives exist, but this is
    #: quite likely always the serial number of the motherboard, and not
    #: something written on the chassis.
    baseboard_serial_number = None
    #: Manufacturer name of Chassis as written in DMI registry
    chassis_manufacturer = None
    #: Chassis type according to DMI registry
    chassis_type = None
    #: Chassis serial number according to DMI registry
    chassis_serial_number = None

    #: lspci raw output
    lspci = None
    #: dmesg raw output
    dmesg = None

    def __setattr__(self, key, value):
        if key == 'disk_controllers' and bool(value):
            raise Exception(value)
        Response.__setattr__(self, key, value)


class DiskController(JSONModel):

    #: Name of device, ata1, ata2 etc.
    dev = ""

    #: False implies it's PATA (IDE)
    sata = False

    #: Raw output from dmesg
    raw_info = ""


class Harddrive(JSONModel):

    #: Device node, e.g. /dev/sda
    dev = ""

    #: False implies it's PATA (IDE)
    sata = False

    #: Manufacturer serial number of the hard drive, if available
    serial = None
    #: Capacity (bytes) of the hard drive
    capacity = None
    #: Manufacturer name
    manufacturer = None
    #: Type of controller ("SSD" / "HDD")
    controller_type = None

    #: Raw smartmontools output
    smart_raw = None
    #: Raw command output
    hdparm_raw = None
    #: Raw command output
    sdparm_raw = None
    #: Raw command output
    blockdev_raw = None
    #: Raw command output
    sysblock_raw = None


class Battery(JSONModel):
    """
    read about ``/sys/class/power_supply/BAT0``
    """

    #: 0-100 capacity
    capacity = None
    #: Kenel's capcity level
    capacity_name = None
    #: Last known watt capacity
    energy_full = None
    #: Designed watt capacity
    energy_full_design = None
    #: Current watt capacity
    energy_now = None
    #: Battery model name
    model_name = None
    #: Technology, for instance Li-ion
    technology = None


class MemoryDevice(JSONModel):

    #: Capacity in MB
    capacity_mb = None
    #: Form factor, e.g. SODIMM
    form_factor = None
    #: Type, e.g. DDR3
    type_technology = None
    #: Speed, 1333 = 1333 MHz
    speed_mhz = None
    #: Locator, e.g. ChannelB-DIMM0
    locator = None
    #: Locator bank, e.g. BANK 2
    locator_bank = None
    #: Data width, e.g. 64 (=64 bits)
    data_bits = None
    #: Manufacturer, e.g. Kingston
    manufacturer = None
