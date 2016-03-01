import requests
import urlparse

from api_server.clients.base_client import BaseClient
from api_server.clients.exceptions import ClientResponseError, ClientError, ClientTimeoutError


class DeisClient(BaseClient):

    def __init__(self, deis_url):
        """Create a new ``DeisClient``.

        @type deis_url: str
        """
        self.deis_url = deis_url

    def _request_and_raise(self, method, path, **kwargs):
        """Sends a request to Deis.

        @type method: str
            HTTP method, such as "POST", "GET", "PUT"

        @type path: str
            The extra http path to be appended to the deis URL

        @rtype: requests.Response

        @raise e: ClientResponseError
            if the response status code is not in the [200, 300) range.
        @raise e: ClientTimeoutError
        @raise e: ClientError
        """
        if 'timeout' not in kwargs:
            kwargs['timeout'] = 3
        try:
            resp = requests.request(method, urlparse.urljoin(
                self.deis_url, path), **kwargs)
        except requests.exceptions.Timeout:
            raise ClientTimeoutError
        except requests.exceptions.RequestException:
            raise ClientError
        if not 200 <= resp.status_code < 300:
            raise ClientResponseError(resp)
        return resp

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
        return DeisAuthenticatedClient(self.deis_url, token)

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
