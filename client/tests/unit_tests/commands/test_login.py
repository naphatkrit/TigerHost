# NOTE: this is a separate file because it needs to mock a different
# instance of ApiClient
import mock
import pytest

from tigerhost.api_client import ApiClient, ApiClientAuthenticationError
from tigerhost.entry import entry


@pytest.yield_fixture(scope='function')
def fake_api_client():
    mocked = mock.Mock(spec=ApiClient)

    def new(api_server_url, username, api_key):
        return mocked
    with mock.patch('tigerhost.commands.user.ApiClient', new=new):
        yield mocked


def test_login_success(runner, fake_api_client):
    result = runner.invoke(entry, ['login', '-u', 'username', '-a', 'key'])
    assert result.exit_code == 0


def test_login_failure_auth(runner, fake_api_client):
    fake_api_client.test_api_key.side_effect = ApiClientAuthenticationError(
        None)
    result = runner.invoke(entry, ['login', '-u', 'username', '-a', 'key'])
    assert result.exit_code == 2
    assert 'Please try again' in result.output


def test_login_failure(runner, fake_api_client):
    fake_api_client.test_api_key.side_effect = Exception
    result = runner.invoke(entry, ['login', '-u', 'username', '-a', 'key'])
    assert result.exit_code == -1
