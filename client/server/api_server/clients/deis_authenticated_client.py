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

    def unset_application_env_variables(self, app_id, env_vars):
        """Unset the environmental variables for the specified app ID

        @type app_id: str

        @type env_vars: list
            The list of variables to unset

        @raises e: DeisClientResponseError
        """
        self._request_and_raise('POST', 'v1/apps/{}/config/'.format(app_id), json={
            'values': {key: None for key in env_vars}
        })

    def get_application_env_variables(self, app_id):
        """Get the environmental variables for the specified app ID.

        @type app_id: str

        @rtype: dict
            The key-value pair representing the environmental variables

        @raises e: DeisClientResponseError
        """
        resp = self._request_and_raise(
            'GET', 'v1/apps/{}/config/'.format(app_id))
        return resp.json()['values']

    def get_application_domains(self, app_id):
        """Get all domains associated with the specified app ID.

        @type app_id: str

        @rtype: list
            List of domains (str)

        @raises e: DeisClientResponseError
        """
        # TODO may have to page
        resp = self._request_and_raise(
            'GET', 'v1/apps/{}/domains/'.format(app_id))
        return [x['domain'] for x in resp.json()['results']]

    def add_application_domain(self, app_id, domain):
        """Add a new domain to the specified app ID.

        @type app_id: str
        @type domain: str

        @raises e: DeisClientResponseError
        """
        self._request_and_raise(
            'POST', 'v1/apps/{}/domains/'.format(app_id), json={'domain': domain})

    def remove_application_domain(self, app_id, domain):
        """Remove a domain from the specified app ID.

        @type app_id: str
        @type domain: str

        @raises e: DeisClientResponseError
        """
        self._request_and_raise(
            'DELETE', 'v1/apps/{}/domains/{}'.format(app_id, domain))

    def get_application_owner(self, app_id):
        """Get the username of the owner of the specified app ID.

        @type app_id: str

        @rtype: str

        @raises e: DeisClientResponseError
        """
        resp = self._request_and_raise('GET', 'v1/apps/{}/'.format(app_id))
        return resp.json()['owner']

    def set_application_owner(self, app_id, username):
        """Set the owner of the application to be the specified username.
        Can only be done by someone with admin privilege on this application.

        @type app_id: str
        @type username: str

        @raises e: DeisClientResponseError
        """
        self._request_and_raise('POST', 'v1/apps/{}/'.format(app_id), json={
            'owner': username
        })

    def get_application_collaborators(self, app_id):
        """Returns the list of users sharing this application.
        This does NOT include the application owner.

        @type app_id: str

        @rtype: list
            The list of usernames of collaborators (str)

        @raises e: DeisClientResponseError
        """
        resp = self._request_and_raise(
            'GET', 'v1/apps/{}/perms/'.format(app_id))
        return resp.json()['users']

    def add_application_collaborator(self, app_id, username):
        """Adds the user with the specified username to the list of
        collaborators

        @type app_id: str
        @type username: str

        @raises e: DeisClientResponseError
        """
        self._request_and_raise('POST', 'v1/apps/{}/perms/'.format(app_id), json={
            'username': username
        })

    def remove_application_collaborator(self, app_id, username):
        """Removes the user with the specified username from the list of
        collaborators

        @type app_id: str
        @type username: str

        @raises e: DeisClientResponseError
        """
        self._request_and_raise(
            'DELETE', 'v1/apps/{}/perms/{}'.format(app_id, username))

    def get_keys(self):
        """Get all public keys associated with this user.

        @rtype: dict
            A dictionary with two keys: 'key_name' and 'key'

        @raises e: DeisClientResponseError
        """
        # TODO may have to page
        resp = self._request_and_raise(
            'GET', 'v1/keys/')
        return [{'key_name': x['id'], 'key': x['public']} for x in resp.json()['results']]

    def add_key(self, key_name, key):
        """Add a public key to this user.

        @type key_name: str
            An ID to be associated with this key

        @type key: str

        @raises e: DeisClientResponseError
        """
        self._request_and_raise('POST', 'v1/keys/', json={
            'id': key_name,
            'public': key
        })

    def remove_key(self, key_name):
        """Remove the specified key from this user.

        @type key_name: str
            The ID associated with this key when added.

        @raises e: DeisClientResponseError
        """
        self._request_and_raise('DELETE', 'v1/keys/{}'.format(key_name))
