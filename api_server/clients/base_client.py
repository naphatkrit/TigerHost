import requests
import urlparse

from api_server.clients.exceptions import ClientResponseError, ClientError, ClientTimeoutError


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

        @raise e: ClientResponseError
            if the response status code is not in the [200, 300) range.
        @raise e: ClientTimeoutError
        @raise e: ClientError
        """
        if 'timeout' not in kwargs:
            kwargs['timeout'] = 3
        try:
            resp = requests.request(method, urlparse.urljoin(
                self.provider_url, path), **kwargs)
        except requests.exceptions.Timeout:
            raise ClientTimeoutError
        except requests.exceptions.RequestException:
            raise ClientError
        if not 200 <= resp.status_code < 300:
            raise ClientResponseError(resp)
        return resp

    def register(self, username, password, email):
        """Register a new user with the provider.

        @type username: str
        @type password: str
        @type email: str

        @raise e: ClientResponseError
        """
        raise NotImplementedError

    def login(self, username, password):
        """Login to the provider and return an authenticated client.

        @type username: str
        @type password: str

        @rtype: api_server.client.base_authenticated_client.AuthenticatedClient

        @raise e: ClientResponseError
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

        @raise e: ClientResponseError
        """
        try:
            return self.login(username, password), False
        except ClientResponseError:
            self.register(username, password, email)
            return self.login(username, password), True
