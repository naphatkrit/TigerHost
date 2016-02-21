import requests
import urlparse

from api_server.clients.deis_client_errors import DeisClientResponseError


class DeisClient:

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
        """
        return requests.request(method, urlparse.urljoin(self.deis_url, path), **kwargs)

    def register(self, username, password, email):
        """Register a new user with Deis.

        @type username: str
        @type password: str
        @type email: str
        """
        resp = self._request('POST', 'v1/auth/register/', json={
            "username": username,
            "password": password,
            "email": email
        })
        if resp.status_code != 201:
            raise DeisClientResponseError(resp)
