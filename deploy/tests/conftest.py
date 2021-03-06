import mock
import os
import pytest

from click.testing import CliRunner
from temp_utils.contextmanagers import temp_dir, chdir
from click_extensions import private_dir

from deploy import settings
from deploy.secret.secret_dir import ensure_secret_dir_exists


@pytest.yield_fixture(scope='function', autouse=True)
def fake_private_dir():
    with temp_dir() as path:
        new_private_dir = os.path.join(path, '.deploy')
        with mock.patch('click_extensions.private_dir.private_dir_path') as mocked:
            mocked.return_value = new_private_dir
            yield


@pytest.fixture(scope='function', autouse=True)
def ensure_private_dir(fake_private_dir):
    private_dir.ensure_private_dir_exists(settings.APP_NAME)


@pytest.fixture(scope='function', autouse=True)
def ensure_secret_dir(fake_private_dir):
    ensure_secret_dir_exists()


@pytest.yield_fixture(scope='function')
def runner():
    runner = CliRunner()
    with runner.isolated_filesystem():
        yield runner


@pytest.yield_fixture(scope='function')
def fake_git_remote():
    with temp_dir() as temp:
        with chdir(temp):
            assert not os.system('git init')
            assert not os.system('touch a && git add . && git commit -m a')
        yield temp
