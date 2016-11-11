"""
Test functions that invoke system commands
"""
import logging

from . import utils

logger = logging.getLogger(__name__)


def test_lspci():
    from lcrs_embedded.system.lspci import lspci_analysis
    from lcrs_embedded.models import ScanResult

    scan_result = ScanResult()
    lspci_analysis(scan_result, mock=utils.IS_CI)
    for k, v in lspci_analysis.expected_results.items():  # @UndefinedVariable
        assert v == scan_result[k]


def test_dmesg():
    from lcrs_embedded.system.dmesg import dmesg_analysis
    from lcrs_embedded.models import ScanResult

    scan_result = ScanResult()
    dmesg_analysis(scan_result)
    logger.debug(scan_result)
    logger.debug(scan_result['disk_controllers'])
    for k, v in dmesg_analysis.expected_results.items():  # @UndefinedVariable
        assert v == scan_result[k]
