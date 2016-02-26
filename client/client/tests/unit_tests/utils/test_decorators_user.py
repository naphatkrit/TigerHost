import click
import mock
import pytest

from tigerhost.api_client import ApiClientAuthenticationError, ApiClient
from tigerhost.user import User, save_user
from tigerhost.utils import decorators


@pytest.yield_fixture(scope='function')
def fake_api_client():
    mocked = mock.Mock(spec=ApiClient)

    def new(api_server_url, username, api_key):
        return mocked
    with mock.patch('tigerhost.utils.decorators.ApiClient', new=new):
        yield mocked


@pytest.fixture(scope='function')
def saved_user(ensure_private_dir):
    user = User(username='username', api_key='key')
    save_user(user)


class ErrorA(Exception):
    pass


class ErrorB(Exception):
    pass


@click.command()
@decorators.pass_user
def sample_cmd(user):
    pass


def test_no_user(runner):
    result = runner.invoke(sample_cmd)
    assert result.exit_code == 2


def test_failed_auth(runner, fake_api_client, saved_user):
    fake_api_client.test_api_key.side_effect = ApiClientAuthenticationError(
        None)
    result = runner.invoke(sample_cmd)
    assert result.exit_code == 2


def test_success(runner, fake_api_client, saved_user):
    result = runner.invoke(sample_cmd)
    assert result.exit_code == 0
