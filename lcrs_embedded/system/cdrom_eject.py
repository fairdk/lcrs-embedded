import logging

from ..utils.decorators import run_command

logger = logging.getLogger(__name__)


def eject(scan_result, *args, **kwargs):
    """

    """
    if not scan_result.cdrom:
        logger.info("No CD drive found to eject")
        return

    command = "eject /dev/{}".format(scan_result.cdrom_drive_name)

    @run_command(command, mock_in_test=True)
    def _eject(scan_result, stdout, stderr, succeeded):
        if succeeded:
            logger.info("CD drive successfully ejected")
            scan_result.cdrom_ejected = True
        else:
            logger.error("Couldn't eject CD drive: {}".format(command))
            scan_result.cdrom_ejected = False
    _eject.mock_output = ""

    return _eject(scan_result, *args, **kwargs)
