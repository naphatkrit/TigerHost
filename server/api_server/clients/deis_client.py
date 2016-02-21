import requests
import urlparse

from api_server.clients.deis_client_errors import DeisClientResponseError


class DeisClient:

    def __init__(self, deis_url):
        """Create a new ``DeisClient``.

        @type deis_url: str
        """
        self.deis_url = deis_url

    def register(self, username, password, email):
        """Register a new user with Deis.

        @type username: str
        @type password: str
        @type email: str
        """
        url = urlparse.urljoin(self.deis_url, 'v1/auth/register/')
        resp = requests.post(url, json={
            "username": username,
            "password": password,
            "email": email
        })
        if resp.status_code != 201:
            raise DeisClientResponseError(resp)
