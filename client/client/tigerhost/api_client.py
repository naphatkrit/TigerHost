import requests
import urlparse

from wsse import WSSEAuth


class ApiClientResponseError(Exception):

    def __init__(self, response):
        """Create a new ``ApiClientResponseError``.

        @type response: requests.Response
        """
        self.response = response

    def __unicode__(self):
        return """Response Code {code}

        {body}
        """.format(code=self.response.status_code, body=self.response.json())


class ApiClientAuthenticationError(ApiClientResponseError):
    pass


class ApiClient(object):

    def __init__(self, api_server_url, username, api_key):
        """Create a new ``ApiClient``.

        @type api_server_url: str
        @type username: str
        @type api_key: str
        """
        self.api_server_url = api_server_url
        self.username = username
        self.api_key = api_key

    def _request_and_raise(self, method, path, **kwargs):
        """Sends a request to the api server.

        @type method: str
            HTTP method, such as "POST", "GET", "PUT"

        @type path: str
            The extra http path to be appended to the deis URL

        @rtype: requests.Response

        @raise e: ApiClientAuthenticationError
            if the response status code is 401

        @raise e: ApiClientResponseError
            if the response status code is not 401 and not in the [200, 300) range.
        """
        resp = requests.request(method, urlparse.urljoin(
            self.api_server_url, path), auth=WSSEAuth(self.username, self.api_key), **kwargs)
        if resp.status_code == 401:
            raise ApiClientAuthenticationError(resp)
        if not 200 <= resp.status_code < 300:
            raise ApiClientResponseError(resp)
        return resp

    def get_all_applications(self):
        """Get all application IDs associated with this user.

        @rtype: list
        """
        resp = self._request_and_raise('GET', 'api/v1/apps')
        return resp.json()['results']
