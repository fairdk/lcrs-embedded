"""
Reading the API exposed in /sys/class/power_supply/BAT0
"""
import logging

from .. import models
from ..utils.decorators import readfile

logger = logging.getLogger(__name__)


def bat0(scan_result, mock_failure=None):
    """
    Calls all the utility functions that'll read virtual /sys files about
    battery API
    """

    _bat0_present(scan_result, mock_failure=mock_failure)

    if scan_result.battery:
        _bat0_capacity(scan_result)
        _bat0_capacity_name(scan_result)
        _bat0_energy_full(scan_result)
        _bat0_energy_full_design(scan_result)
        _bat0_model_name(scan_result)
        _bat0_technology(scan_result)


@readfile("/sys/class/power_supply/BAT0/present", mock_in_test=True)
def _bat0_present(scan_result, file_contents, readable):
    """
    Reads memory information, but only in case DMI data collection has not
    produced a reliable memory_total.
    """
    if not scan_result.battery:
        scan_result.battery = models.Battery()
    battery_present = file_contents.strip() == "1"
    if not battery_present:
        scan_result.battery = None

_bat0_present.mock_output = """1"""
_bat0_present.expected_result = {
    'battery': models.Battery()
}


def battery_file_factory(
        name, attr_name, mock_output, mock_result, is_int=False):
    """
    Factory function for battery
    """

    @readfile("/sys/class/power_supply/BAT0/" + name, mock_in_test=True)
    def func(scan_result, file_contents, readable):
        """
        Reads memory information, but only in case DMI data collection has not
        produced a reliable memory_total.
        """
        result = file_contents.strip()
        if is_int:
            try:
                result = int(result)
            except TypeError:
                result = None
        return result

    func.mock_output = mock_output
    func.expected_result = {
        'battery': models.Battery(**{attr_name: mock_result})
    }
    return func

_bat0_capacity = battery_file_factory(
    "capacity_",
    "capacity",
    "50",
    50,
    is_int=True
)

_bat0_capacity_name = battery_file_factory(
    "capacity_level",
    "capacity_name",
    "Normal",
    "Normal",
    is_int=False
)

_bat0_energy_full = battery_file_factory(
    "energy_full",
    "energy_full",
    "12345",
    12345,
    is_int=True
)

_bat0_energy_full_design = battery_file_factory(
    "energy_full_design",
    "energy_full_design",
    "12345",
    12345,
    is_int=True
)

_bat0_energy_now = battery_file_factory(
    "energy_now",
    "energy_now",
    "12345",
    12345,
    is_int=True
)

_bat0_model_name = battery_file_factory(
    "model_name",
    "model_name",
    "AKSDJ123",
    "AKSDJ123",
    is_int=False
)

_bat0_technology = battery_file_factory(
    "technology",
    "technology",
    "Li-ion",
    "Li-ion",
    is_int=False
)
