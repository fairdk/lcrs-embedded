"""
The protocol itself is embedded in JSON requests transmitted through an HTTP
server.

All classes in this module are fully serializable back and forth.

These are the states of an embedded server and can be observed by the
requesting attendant client.

"""
from .utils.models import JSONModel

STATE_IDLE = "IDLE"
STATE_BUSY = "BUSY"
STATE_FAIL = "FAIL"
STATE_DISCONNECTED = "DISCONNECTED"

STATES = set((
    STATE_IDLE,
    STATE_FAIL,
    STATE_BUSY,
    STATE_DISCONNECTED,
))
"""
States of the slave application::
    IDLE: Denotes that the client can handle new requests (jobs)
    BUSY: Denotes that a client will reject requests (jobs)
    FAIL: Latest request failed, new requests are accepted
    DISCONNECTED: Both locally and remote, network connection is not
    available.
"""

#: Valid command IDs
COMMANDS = set((
    "SCAN",  # Start scanning for hardware
    "WIPE",  # Start wiping
    "STATUS",  # Get current status (state, progress)
    "HARDWARE",  # Get results from SCAN command
    "SHELL_EXEC",  # Execute a single command and return command ID
    "SHELL_RESULTS",  # Get results of a command ID
    "BADBLOCKS",  # Scan for bad blocks
    "DEBUG_MODE",  # Switch on debug mode
    "RESET",
))


class Command:

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


class ScanResponse(Response):
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
    ethernet = []
    wifi = []
    is_laptop = False
    total_memory = None
    manufacturer = None


class Processor(JSONModel):

    family = None
    name = None
    cores = None


class Harddrive(JSONModel):

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
