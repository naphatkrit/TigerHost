import os
import pytest
import shutil
import tempfile

from tigerhost.utils import contextmanagers


@pytest.yield_fixture(scope='function')
def temp_dir():
    path = tempfile.mkdtemp()
    try:
        yield path
    finally:
        shutil.rmtree(path)


def test_chdir(temp_dir):
    current = os.getcwd()
    with contextmanagers.chdir(temp_dir):
        assert os.path.realpath(os.getcwd()) == os.path.realpath(temp_dir)
    assert os.getcwd() == current


def test_temp_dir():
    with contextmanagers.temp_dir() as temp_dir:
        assert os.path.exists(temp_dir)
        assert os.path.isdir(temp_dir)
    assert not os.path.exists(temp_dir)
