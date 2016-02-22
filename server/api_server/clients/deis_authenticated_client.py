from api_server.clients.deis_client import DeisClient


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

    def _request_and_raise(self, *args, **kwargs):
        if 'headers' not in kwargs:
            kwargs['headers'] = {}
        kwargs['headers']['Authorization'] = 'token {}'.format(self.token)
        return super(self.__class__, self)._request_and_raise(*args, **kwargs)

    def get_all_applications(self):
        """Get all application IDs associated with this user.

        @rtype: list
            The list of application IDs (str)

        @raises DeisClientResponseError
        """
        # TODO this may not work correctly if there are too many apps
        # will need to look at "next" key in the response
        resp = self._request_and_raise('GET', 'v1/apps')
        return [x['id'] for x in resp.json()['results']]

    def create_application(self, app_id):
        """Create a new application with the specified ID.

        @type app_id: str

        @raises DeisClientResponseError
        """
        self._request_and_raise('POST', 'v1/apps/', json={
            'id': app_id
        })

    def delete_application(self, app_id):
        """Delete an application with the specified ID.

        @type app_id: str

        @raises DeisClientResponseError
        """
        self._request_and_raise('DELETE', 'v1/apps/{}/'.format(app_id))

    def set_application_env_variables(self, app_id, bindings):
        """Set the environmental variables for the specified app ID.

        @type app_id: str

        @type bindings: dict
            The key-value pair to set in the environmental.

        @raises DeisClientResponseError
        """
        self._request_and_raise('POST', 'v1/apps/{}/config/'.format(app_id), json={
            'values': bindings
        })
