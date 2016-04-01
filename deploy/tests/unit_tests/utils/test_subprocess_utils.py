import pytest
import subprocess32 as subprocess

from deploy.utils.subprocess_utils import check_call_realtime


def test_check_call_realtime_success():
    lines = ''
    for l in check_call_realtime(['printf', 'hello\nworld\n123']):
        lines += l

    assert lines == 'hello\nworld\n123'


def test_check_call_realtime_failure():
    lines = ''
    with pytest.raises(subprocess.CalledProcessError) as e:
        for l in check_call_realtime(['make', 'doesnotexist']):
            lines += l
    assert e.value.returncode != 0
    assert e.value.cmd == ['make', 'doesnotexist']
    assert len(lines) != 0
