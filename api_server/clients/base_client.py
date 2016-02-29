import requests
import urlparse

from api_server.clients.deis_client_errors import DeisClientResponseError, DeisClientError, DeisClientTimeoutError


class BaseClient(object):

    def __init__(self, url):
        """Create a new ``BaseClient``.

        @type url: str
        """
        self.provider_url = url

    def _request_and_raise(self, method, path, **kwargs):
        """Sends a request to the provider.

        @type method: str
            HTTP method, such as "POST", "GET", "PUT"

        @type path: str
            The extra http path to be appended to the provider URL

        @rtype: requests.Response

        @raise e: DeisClientResponseError
            if the response status code is not in the [200, 300) range.
        @raise e: DeisClientTimeoutError
        @raise e: DeisClientError
        """
        if 'timeout' not in kwargs:
            kwargs['timeout'] = 3
        try:
            resp = requests.request(method, urlparse.urljoin(
                self.provider_url, path), **kwargs)
        except requests.exceptions.Timeout:
            raise DeisClientTimeoutError
        except requests.exceptions.RequestException:
            raise DeisClientError
        if not 200 <= resp.status_code < 300:
            raise DeisClientResponseError(resp)
        return resp

    def register(self, username, password, email):
        """Register a new user with the provider.

        @type username: str
        @type password: str
        @type email: str

        @raise e: DeisClientResponseError
        """
        raise NotImplementedError

    def login(self, username, password):
        """Login to the provider and return an authenticated client.

        @type username: str
        @type password: str

        @rtype: api_server.client.base_authenticated_client.AuthenticatedClient

        @raise e: DeisClientResponseError
        """
        return NotImplementedError

    def login_or_register(self, username, password, email):
        """Try to log the user in. If the user has not been created yet, then
        attempt to register the user and then log in.

        @type username: str
        @type password: str
        @type email: str

        @rtype: tuple
            (api_server.client.base_authenticated_client.AuthenticatedClient, bool) - the bool is true if a new user
            was registered with the provider

        @raise e: DeisClientResponseError
        """
        try:
            return self.login(username, password), False
        except DeisClientResponseError:
            self.register(username, password, email)
            return self.login(username, password), True
