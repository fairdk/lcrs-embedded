"""
Test functions that invoke system commands
"""
import logging

from . import utils

logger = logging.getLogger(__name__)


def test_lspci():
    """
    This test is only mocked on CI
    """
    from lcrs_embedded.system.lspci import lspci_analysis
    from lcrs_embedded.models import ScanResult

    scan_result = ScanResult()
    lspci_analysis(scan_result, mock=utils.IS_CI)

    if utils.IS_CI:
        for k, v in lspci_analysis.expected_results.items():  # @UndefinedVariable  # noqa
            assert v == scan_result[k]
    else:
        assert bool(scan_result.graphics_controller)
        assert bool(scan_result.wifi)
        assert bool(scan_result.ethernet)
        assert bool(scan_result.has_usb)


def test_dmesg():
    """
    This test is always mocked
    """
    from lcrs_embedded.system.dmesg import dmesg_analysis
    from lcrs_embedded.models import ScanResult

    scan_result = ScanResult()

    dmesg_analysis(scan_result)
    for k, v in dmesg_analysis.expected_results.items():  # @UndefinedVariable
        assert v == scan_result[k]


def test_dmidecode_system():
    """
    This test is always mocked
    """
    from lcrs_embedded.system.dmidecode import dmidecode_system
    from lcrs_embedded.models import ScanResult

    scan_result = ScanResult()
    dmidecode_system(scan_result)
    for k, v in dmidecode_system.expected_results.items():  # @UndefinedVariable  # noqa
        assert v == scan_result[k]


def test_command_timeout():
    """
    This test is always mocked
    """
    from lcrs_embedded.utils.decorators import run_command_with_timeout

    @run_command_with_timeout("sleep 10", timeout=0.2)
    def test(stdout, stderr, succeeded):
        assert not succeeded

    test()