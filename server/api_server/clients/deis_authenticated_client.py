from api_server.clients.deis_client import DeisClient
from api_server.clients.deis_client_errors import DeisClientResponseError


class DeisAuthenticatedClient(DeisClient):
    """The Deis client for API that requires authentication
    """

    def __init__(self, deis_url, token):
        """Create a new ``DeisAuthenticatedClient``.

        @type deis_url: str

        @type token: str
            Authentication token for this user.
        """
        super(self.__class__, self).__init__(deis_url)
        self.token = token


    def _request(self, *args, **kwargs):
        if 'headers' not in kwargs:
            kwargs['headers'] = {}
        kwargs['headers']['Authorization'] = 'token {}'.format(self.token)
        return super(self.__class__, self)._request(*args, **kwargs)


    def get_all_applications(self):
        """Get all application IDs associated with this user.

        @rtype: list
            The list of application IDs (str)

        @raises DeisClientResponseError
        """
        # TODO this may not work correctly if there are too many apps
        # will need to look at "next" key in the response
        resp = self._request('GET', 'v1/apps')
        if resp.status_code != 200:
            raise DeisClientResponseError(resp)
        return [x['id'] for x in resp.json()['results']]


    def create_application(self, app_id):
        """Create a new application with the specified ID.

        @type app_id: str

        @raises DeisClientResponseError
        """
        resp = self._request('POST', 'v1/apps/')
        if resp.status_code != 201:
            raise DeisClientResponseError(resp)
