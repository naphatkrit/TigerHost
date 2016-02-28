import os
import pytest

from tigerhost.entry import entry
from tigerhost.utils import contextmanagers


@pytest.fixture(scope='function')
def logged_in_user(runner, username, api_key, ensure_private_dir):
    result = runner.invoke(entry, ['login', '-u', username, '-a', api_key])
    assert result.exit_code == 0


@pytest.yield_fixture(scope='function')
def make_app(runner, logged_in_user, app_id):
    os.makedirs(app_id)
    with contextmanagers.chdir(app_id):
        assert not os.system('git init')
        result = runner.invoke(entry, ['create', app_id])
        assert result.exit_code == 0
        yield
