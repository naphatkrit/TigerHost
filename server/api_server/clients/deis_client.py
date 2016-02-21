import requests
import urlparse

from api_server.clients.deis_client_errors import DeisClientResponseError


class DeisClient(object):

    def __init__(self, deis_url):
        """Create a new ``DeisClient``.

        @type deis_url: str
        """
        self.deis_url = deis_url

    def _request(self, method, path, **kwargs):
        """Sends a request to Deis.

        @type method: str
            HTTP method, such as "POST", "GET", "PUT"

        @type path: str
            The extra http path to be appended to the deis URL

        @rtype: requests.Response
        """
        return requests.request(method, urlparse.urljoin(self.deis_url, path), **kwargs)

    def register(self, username, password, email):
        """Register a new user with Deis.

        @type username: str
        @type password: str
        @type email: str

        @raise e: DeisClientResponseError
        """
        resp = self._request('POST', 'v1/auth/register/', json={
            "username": username,
            "password": password,
            "email": email
        })
        if resp.status_code != 201:
            raise DeisClientResponseError(resp)

    def login(self, username, password):
        """Login to Deis and return an authenticated client.

        @type username: str
        @type password: str

        @rtype: DeisAuthenticatedClient

        @raise e: DeisClientResponseError
        """
        # this avoids circular imports
        from api_server.clients.deis_authenticated_client import DeisAuthenticatedClient

        resp = self._request('POST', 'v1/auth/login/', json={
            "username": username,
            "password": password
        })
        if resp.status_code != 201:
            raise DeisClientResponseError(resp)
        token = resp.json()['token']
        return DeisAuthenticatedClient(self.deis_url, token)
