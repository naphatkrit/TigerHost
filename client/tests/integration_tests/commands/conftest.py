import pytest

from tigerhost.entry import entry


@pytest.fixture(scope='function')
def logged_in_user(runner, username, api_key, ensure_private_dir):
    result = runner.invoke(entry, ['login', '-u', username, '-a', api_key])
    assert result.exit_code == 0
