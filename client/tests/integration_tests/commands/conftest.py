import pytest

from tigerhost.entry import entry


@pytest.fixture(scope='function')
def logged_in_user(runner, username, api_key, ensure_private_dir):
    result = runner.invoke(entry, ['login', '-u', username, '-a', api_key])
    assert result.exit_code == 0


@pytest.yield_fixture(scope='function')
def make_app(runner, make_git_repo, logged_in_user, app_id):
    result = runner.invoke(entry, ['create', app_id])
    assert result.exit_code == 0
    try:
        yield
    finally:
        runner.invoke(entry, ['apps:destroy', '--app', app_id])


@pytest.fixture(scope='function')
def backend(api_client):
    return api_client.get_backends()['default']
