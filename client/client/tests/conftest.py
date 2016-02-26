import mock
import os
import pytest

from click.testing import CliRunner

from tigerhost.private_dir import ensure_private_dir_exists
from tigerhost.utils.contextmanagers import temp_dir


@pytest.yield_fixture(scope='function')
def runner():
    runner = CliRunner()
    with runner.isolated_filesystem():
        assert not os.system('git init')
        os.mkdir('.git/tigerhost')
        yield runner


@pytest.yield_fixture(scope='function', autouse=True)
def fake_private_dir():
    with temp_dir() as path:
        new_private_dir = os.path.join(path, '.tigerhost')
        with mock.patch('tigerhost.private_dir._private_dir_path', new=new_private_dir):
            yield


@pytest.fixture(scope='function')
def ensure_private_dir(fake_private_dir):
    ensure_private_dir_exists()
