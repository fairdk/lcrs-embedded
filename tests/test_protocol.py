import json
import pytest
from tests.utils import compare_dictionaries


def test_model():
    from lcrs_embedded import models
    with pytest.raises(KeyError):
        models.Harddrive(asdjkjklasd=12123)


def test_serialization():
    from lcrs_embedded import models

    scan_response = models.ScanResult()
    scan_response.battery = models.Battery(capacity=29, energy_full=100000)
    scan_response.total_memory = 123
    scan_response.harddrives = [
        models.Harddrive(serial="Xyz123")
    ]

    json_s = str(json.dumps(scan_response))

    assert compare_dictionaries(scan_response, json.loads(json_s))
