import pytest

from lcrs_embedded.utils import validation


def test_validation():

    with pytest.raises(TypeError):
        validation.clean_int("ads 123 123")

    assert validation.clean_int("") is None
