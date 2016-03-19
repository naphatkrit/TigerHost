from api_server.clients.base_client import BaseClient
from api_server.clients.exceptions import ClientResponseError


class DeisClient(BaseClient):

    def register(self, username, password, email):
        """Register a new user with Deis.

        @type username: str
        @type password: str
        @type email: str

        @raise e: ClientResponseError
        """
        self._request_and_raise('POST', 'v1/auth/register/', json={
            "username": username,
            "password": password,
            "email": email
        })

    def login(self, username, password):
        """Login to Deis and return an authenticated client.

        @type username: str
        @type password: str

        @rtype: DeisAuthenticatedClient

        @raise e: ClientResponseError
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

        @type username: str
        @type password: str
        @type email: str

        @rtype: tuple
            (DeisAuthenticatedClient, bool) - the bool is true if a new user
            was registered with Deis

        @raise e: ClientResponseError
        """
        try:
            return self.login(username, password), False
        except ClientResponseError:
            self.register(username, password, email)
            return self.login(username, password), True
