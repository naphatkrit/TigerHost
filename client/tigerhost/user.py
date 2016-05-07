"""A module to manage the current user"""
import json
import os

from click_extensions import private_dir

from tigerhost import settings


def _user_path():
    """Returns the path to the user file

    :rtype: str
    :returns: path
    """
    return os.path.join(private_dir.private_dir_path(settings.APP_NAME), 'user.json')


class UserFormatError(Exception):
    """When the user json file has a format error
    """
    pass


class User(object):

    def __init__(self, username, api_key):
        """Create a new user.

        :param str username:
        :param str api_key:
        """
        self.username = username
        self.api_key = api_key

    def to_json(self):
        """Serialize the user into a json string.

        :rtype: str
        """
        return json.dumps({
            'username': self.username,
            'api_key': self.api_key,
        })

    @classmethod
    def from_json(cls, json_string):
        """Create a new user from the json string.

        :param str json_string:

        :rtype: User
        """
        try:
            data = json.loads(json_string)
        except ValueError:
            raise UserFormatError
        if 'username' not in data or 'api_key' not in data:
            raise UserFormatError
        return cls(username=data['username'], api_key=data['api_key'])

    def __eq__(self, other):
        return self.username == other.username and self.api_key == other.api_key


def save_user(user):
    """Save user to the private directory

    :param User user:
    """
    json_string = user.to_json()
    with open(_user_path(), 'w') as f:
        f.write(json_string)


def has_saved_user():
    """Check if a user has been saved.

    :rtype: bool
    """
    return os.path.exists(_user_path())


def delete_user():
    """Delete the saved user account. Must be logged in.
    """
    os.remove(_user_path())


def load_user():
    """Load the user from the saved location.

    :rtype: User
    """
    assert has_saved_user()
    with open(_user_path(), 'r') as f:
        json_string = f.read()
    return User.from_json(json_string)
