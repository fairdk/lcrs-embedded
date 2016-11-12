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
    YAGNI mentality: Try to make stuff that's simple, dump advanced stuff into
    raw output and improve the protocol in the future.

    Because the UI and the embedded server are usually bundled, we don't need
    to worry about things breaking.
    """

    processor = {}
    battery = {}
    harddrives = []
    screen = {}
    removable_drives = []
    ethernet = ""
    wifi = ""
    is_laptop = False
    total_memory = None
    graphics_controller = ""
    usb_controller = ""
    has_usb = False
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

    def __setattr__(self, key, value):
        if key == 'disk_controllers' and bool(value):
            raise Exception(value)
        Response.__setattr__(self, key, value)


class Processor(JSONModel):

    family = None
    name = None
    cores = None


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

    #: 0-100 capacity
    capacity = None
    #: Kenel's capcity level, read about ``/sys/class/power_supply/BAT0``
    capacity_name = None
    #: Last known watt capacity, read about ``/sys/class/power_supply/BAT0``
    energy_full = None
    #: Designed watt capacity, read about ``/sys/class/power_supply/BAT0``
    energy_full_design = None
    #: Battery model name, read about ``/sys/class/power_supply/BAT0``
    model_name = None
    #: Technology, for instance Li-ion
    #: Read about ``/sys/class/power_supply/BAT0``
    technologi = None
