import mock
import pytest

from tigerhost.api_client import ApiClient
from tigerhost.user import User, save_user


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
