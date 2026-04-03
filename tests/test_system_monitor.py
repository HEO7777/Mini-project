import pytest
import pandas as pd
from system_monitor import has_valid_pid, terminate_pid


def test_has_valid_pid_invalid_types():
    assert not has_valid_pid(None)
    assert not has_valid_pid("123")
    assert not has_valid_pid(-1)
    assert not has_valid_pid(0)
    assert not has_valid_pid(1)


def test_has_valid_pid_valid():
    assert has_valid_pid(2)


def test_terminate_pid_protected():
    with pytest.raises(PermissionError):
        terminate_pid(1)


@pytest.mark.parametrize("bad_pid", [None, "abc", -5, 0])
def test_terminate_pid_invalid(bad_pid):
    with pytest.raises(ValueError):
        terminate_pid(bad_pid)
