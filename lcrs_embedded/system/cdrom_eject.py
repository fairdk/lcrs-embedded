import logging

from ..utils.decorators import run_command_with_timeout

logger = logging.getLogger(__name__)


def eject(scan_result, *args, **kwargs):
    """
    default_mock = True because dmesg output is different depending on Kernel.
    Ubuntu Kernel does not report logical blocks/hardware sectors.
    """
    if not scan_result.cdrom:
        logger.info("No CD drive found to eject")
        return

    command = "eject /dev/{}".format(scan_result.cdrom_drive_name)

    @run_command_with_timeout(command, mock_in_test=True)
    def _eject(scan_result, stdout, stderr, succeeded):
        if succeeded:
            logger.info("CD drive successfully ejected")
        else:
            logger.error("Couldn't eject CD drive: {}".format(command))
        scan_result.cdrom_ejected = True

    return _eject(scan_result, *args, **kwargs)
