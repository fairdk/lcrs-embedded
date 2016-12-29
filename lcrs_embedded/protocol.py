"""
Protocol message IDs

For the actual models being transmitted in JSON, refer to lcrs_embedded.json
"""

#: Denotes that the client can handle new requests (jobs)
STATE_IDLE = "IDLE"

#: Denotes that a client will reject requests (jobs)
STATE_BUSY = "BUSY"

#: Latest request failed, new requests are accepted
STATE_FAIL = "FAIL"

#: Both locally and remote, network connection is not available.
STATE_DISCONNECTED = "DISCONNECTED"

#: Allowed states of the slave application
STATES = set((
    STATE_IDLE,
    STATE_FAIL,
    STATE_BUSY,
    STATE_DISCONNECTED,
))


#: Job is still running
JOB_ACTIVE = "ACTIVE"
#: Job has finished with errors
JOB_FAILED = "FAIL"
#: Job has finished correctly
JOB_FINISHED = "FINISHED"
#: Requested job is unknown
JOB_UNKNOWN = "UNKNOW"

#: Allowed states of a job
JOB_STATES = set((
    JOB_ACTIVE,
    JOB_FAILED,
    JOB_FINISHED,
    JOB_UNKNOWN,
))

#: Start scanning for hardware
COMMAND_SCAN = "SCAN"

#: Start wiping
COMMAND_WIPE = "WIPE"

#: Get current status (state, progress)
COMMAND_STATUS = "STATUS"

#: Get results from SCAN command
COMMAND_HARDWARE = "HARDWARE"

#: Execute a single command and return command ID
COMMAND_SHELL_EXEC = "SHELL_EXEC"

#: Get results of a command ID
COMMAND_SHELL_RESULTS = "SHELL_RESULTS"

#: Run badblocks (typically not needed because of S.M.A.R.T.)
COMMAND_BADBLOCKS = "DISKHEALTH"

#: Switch on DEBUG logging
COMMAND_DEBUG = "DEBUG"

#: Fetch log
COMMAND_LOG = "LOG"

#: Kill all jobs and go back to IDLE state
COMMAND_RESET = "RESET"

#: Valid command IDs
COMMANDS = set((
    COMMAND_SCAN,
    COMMAND_WIPE,
    COMMAND_STATUS,
    COMMAND_HARDWARE,
    COMMAND_SHELL_EXEC,
    COMMAND_SHELL_RESULTS,
    COMMAND_BADBLOCKS,
    COMMAND_DEBUG,
    COMMAND_RESET,
))
