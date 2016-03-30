import mock
import os
import pytest

from click.testing import CliRunner
from tigerhost import private_dir
from tigerhost.utils.contextmanagers import temp_dir

from tigerhostctl import settings


@pytest.yield_fixture(scope='function', autouse=True)
def fake_private_dir():
    with temp_dir() as path:
        new_private_dir = os.path.join(path, '.tigerhostctl')
        with mock.patch('tigerhost.private_dir.private_dir_path') as mocked:
            mocked.return_value = new_private_dir
            yield


@pytest.fixture(scope='function', autouse=True)
def ensure_private_dir(fake_private_dir):
    private_dir.ensure_private_dir_exists(settings.APP_NAME)


@pytest.yield_fixture(scope='function')
def runner():
    runner = CliRunner()
    with runner.isolated_filesystem():
        yield runner
