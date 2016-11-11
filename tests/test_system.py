"""
Test functions that invoke system commands
"""

import logging

logger = logging.getLogger(__name__)


def test_lspci():
    from lcrs_embedded.system import lspci_analysis
    from lcrs_embedded.models import ScanResult

    scan_result = ScanResult()
    lspci_analysis(scan_result)
    for k, v in lspci_analysis.expected_results.items():  # @UndefinedVariable
        logger.debug(v)
        logger.debug(getattr(scan_result, k))
        assert v == scan_result[k]
