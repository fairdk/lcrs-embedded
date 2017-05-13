import json

import pytest
from lcrs_embedded.utils.models import decoder
from tests.utils import compare_dictionaries


def test_model():
    from lcrs_embedded import models
    with pytest.raises(KeyError):
        models.Harddrive(asdjkjklasd=12123)

    with pytest.raises(KeyError):
        h = models.Harddrive()
        h.asdkdaskdask = None

    with pytest.raises(NotImplementedError):
        h = models.Harddrive()
        del h['sata']

    def create_list():
        s = models.ScanResult()
        s.disk_controllers.append(models.DiskController())
        s.disk_controllers.append(models.DiskController())
        assert len(s.disk_controllers) == 2
        for controller in s.disk_controllers:
            assert bool(controller)
        assert len(s.disk_controllers) == 2

    # Various tests to ensure that we don't have some immutable stuff or
    # leakage between different instances.
    create_list()
    create_list()


def test_serialization():
    from lcrs_embedded import models

    scan_response = models.ScanResult()
    scan_response.battery = models.Battery(capacity=29, energy_full=100000)
    scan_response.memory_total = 123
    scan_response.harddrives = [
        models.Harddrive(serial="Xyz123")
    ]

    json_s = str(json.dumps(scan_response))
    after_serialization = json.loads(
        json_s,
        object_hook=decoder
    )

    assert compare_dictionaries(scan_response, after_serialization)
