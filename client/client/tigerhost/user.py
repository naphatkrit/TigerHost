import json


class UserFormatError(Exception):
    pass


class User(object):

    def __init__(self, username, api_key):
        """Create a new user.

        @type username: str
        @type api_key: str
        """
        self.username = username
        self.api_key = api_key

    def to_json(self):
        """Serialize the user into a json string.

        @rtype: str
        """
        return json.dumps({
            'username': self.username,
            'api_key': self.api_key,
        })

    @classmethod
    def from_json(cls, json_string):
        """Create a new user from the json string.

        @type json_string: str

        @rtype: User
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
