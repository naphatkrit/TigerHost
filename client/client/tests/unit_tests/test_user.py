import json
import mock
import os
import pytest

from tigerhost.user import User, UserFormatError, save_user, load_user, has_saved_user
from tigerhost.utils.contextmanagers import temp_dir


def test_to_json():
    user = User(username='username', api_key='api_key')
    data = json.loads(user.to_json())
    assert data['username'] == 'username'
    assert data['api_key'] == 'api_key'


def test_from_json():
    data = {
        'username': 'username',
        'api_key': 'api_key',
    }
    user = User.from_json(json.dumps(data))
    assert user.username == 'username'
    assert user.api_key == 'api_key'


def test_from_json_incomplete_data():
    data = {
        'username': 'username',
    }
    with pytest.raises(UserFormatError):
        User.from_json(json.dumps(data))


def test_from_json_malformed_string():
    data = {
        'username': 'username',
        'api_key': 'api_key',
    }
    with pytest.raises(UserFormatError):
        User.from_json(json.dumps(data) + '}')


def test_symmetry():
    user = User(username='username', api_key='api_key')
    assert User.from_json(user.to_json()) == user


@pytest.yield_fixture(scope='function')
def fake_user_path():
    with temp_dir() as path:
        new_user_path = os.path.join(path, 'user.json')
        with mock.patch('tigerhost.user._user_path', new=new_user_path):
            yield


def test_save_user(fake_user_path):
    assert not has_saved_user()
    user = User(username='username', api_key='api_key')
    save_user(user)
    assert has_saved_user()
    assert load_user() == user
