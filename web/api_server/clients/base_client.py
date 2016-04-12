import requests
import urlparse

from api_server.clients.exceptions import ClientResponseError, ClientError, ClientTimeoutError


class BaseClient(object):

    def __init__(self, url):
        """Create a new BaseClient.

        :param str url: the URL to use with this client
        """
        self.backend_url = url

    def _request_and_raise(self, method, path, **kwargs):
        """Sends a request to the backend.

        :param str method: HTTP method, such as "POST", "GET", "PUT"

        :param str path: The extra http path to be appended to the backend URL

        :rtype: requests.Response

        :raises api_server.clients.exceptions.ClientResponseError:
            if the response status code is not in the [200, 300) range.
        :raises api_server.clients.exceptions.ClientTimeoutError:
        :raises api_server.clients.exceptions.ClientError:
        """
        if 'timeout' not in kwargs:
            kwargs['timeout'] = 10
        try:
            resp = requests.request(method, urlparse.urljoin(
                self.backend_url, path), **kwargs)
        except requests.exceptions.Timeout:
            raise ClientTimeoutError
        except requests.exceptions.RequestException:
            raise ClientError
        if not 200 <= resp.status_code < 300:
            raise ClientResponseError(resp)
        return resp

    def register(self, username, password, email):
        """Register a new user with the backend.

        :param str username: The username to register

        :param str password: The password to use for authentication

        :param str email: The email of the user

        :raises api_server.clients.exceptions.ClientError:
        """
        raise NotImplementedError

    def login(self, username, password):
        """Login to the backend and return an authenticated client.

        :param str username: the username to login
        :param str password: the password

        :rtype: api_server.client.base_authenticated_client.AuthenticatedClient

        :raises api_server.clients.exceptions.ClientError:
        """
        return NotImplementedError

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
