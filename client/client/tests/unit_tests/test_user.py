import json
import pytest

from tigerhost.user import User, UserFormatError


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
