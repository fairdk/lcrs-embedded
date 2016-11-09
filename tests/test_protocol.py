import json
import pytest
from tests.utils import compare_dictionaries


def test_model():
    from lcrs_embedded import protocol
    with pytest.raises(KeyError):
        protocol.Harddrive(asdjkjklasd=12123)


def test_serialization():
    from lcrs_embedded import protocol

    scan_response = protocol.ScanResponse()
    scan_response.battery = protocol.Battery(capacity=29, energy_full=100000)
    scan_response.total_memory = 123
    scan_response.harddrives = [
        protocol.Harddrive(serial="Xyz123")
    ]

    json_s = str(json.dumps(scan_response))

    assert compare_dictionaries(scan_response, json.loads(json_s))
