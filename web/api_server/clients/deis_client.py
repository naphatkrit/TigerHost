from api_server.clients.base_client import BaseClient
from api_server.clients.exceptions import ClientResponseError


class DeisClient(BaseClient):

    def register(self, username, password, email):
        """Register a new user with the backend.

        :param str username: The username to register

        :param str password: The password to use for authentication

        :param str email: The email of the user

        :raises api_server.clients.exceptions.ClientError:
        """
        self._request_and_raise('POST', 'v1/auth/register/', json={
            "username": username,
            "password": password,
            "email": email
        })

    def login(self, username, password):
        """Login to the backend and return an authenticated client.

        :param str username: the username to login
        :param str password: the password

        :rtype: api_server.client.base_authenticated_client.AuthenticatedClient

        :raises api_server.clients.exceptions.ClientError:
        """
        # this avoids circular imports
        from api_server.clients.deis_authenticated_client import DeisAuthenticatedClient

        resp = self._request_and_raise('POST', 'v1/auth/login/', json={
            "username": username,
            "password": password
        })
        token = resp.json()['token']
        return DeisAuthenticatedClient(self.backend_url, token)

    def login_or_register(self, username, password, email):
        """Try to log the user in. If the user has not been created yet, then
        attempt to register the user and then log in.

        :param str username: the username
        :param str password: the password
        :param str email: the email, only used when a registration is required

        :rtype: tuple
        :returns: (api_server.client.base_authenticated_client.AuthenticatedClient, bool) - the bool is true if a new user
            was registered with the backend

        :raises api_server.clients.exceptions.ClientError:
        """
        try:
            return self.login(username, password), False
        except ClientResponseError:
            self.register(username, password, email)
            return self.login(username, password), True
