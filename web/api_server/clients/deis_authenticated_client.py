from api_server.clients.base_authenticated_client import BaseAuthenticatedClient
from api_server.clients.deis_client import DeisClient


class DeisAuthenticatedClient(DeisClient, BaseAuthenticatedClient):
    """The Deis client for API that requires authentication
    """

    def __init__(self, deis_url, token):
        """Create a new :code:`DeisAuthenticatedClient`.

        :param str deis_url:
        :param str token: Authentication token for this user.
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

        :rtype: list
        :returns: The list of application IDs (str)

        @raises ClientResponseError
        """
        # TODO this may not work correctly if there are too many apps
        # will need to look at "next" key in the response
        resp = self._request_and_raise('GET', 'v1/apps')
        return [x['id'] for x in resp.json()['results']]

    def create_application(self, app_id):
        """Create a new application with the specified ID.

        :param str app_id: the app ID

        :raises api_server.clients.exceptions.ClientError:
        """
        self._request_and_raise('POST', 'v1/apps/', json={
            'id': app_id
        })

    def delete_application(self, app_id):
        """Delete an application with the specified ID.

        :param str app_id: the app ID

        :raises api_server.clients.exceptions.ClientError:
        """
        self._request_and_raise('DELETE', 'v1/apps/{}/'.format(app_id))

    def set_application_env_variables(self, app_id, bindings):
        """Set the environmental variables for the specified app ID. To unset a variable, set it to ``None``.

        :param str app_id: the app ID
        :param dict bindings: The key-value pair to set in the environment.

        :raises api_server.clients.exceptions.ClientError:
        """
        self._request_and_raise('POST', 'v1/apps/{}/config/'.format(app_id), json={
            'values': bindings
        }, timeout=None)

    def get_application_env_variables(self, app_id):
        """Get the environmental variables for the specified app ID.

        :param str app_id: the app ID

        :rtype: dict
        :returns: The key-value pair representing the environmental variables

        :raises api_server.clients.exceptions.ClientError:
        """
        resp = self._request_and_raise(
            'GET', 'v1/apps/{}/config/'.format(app_id))
        return resp.json()['values']

    def get_application_domains(self, app_id):
        """Get all domains associated with the specified app ID.

        :param str app_id: the app ID

        :rtype: list
        :returns: List of domains (str)

        :raises api_server.clients.exceptions.ClientError:
        """
        # TODO may have to page
        resp = self._request_and_raise(
            'GET', 'v1/apps/{}/domains/'.format(app_id))
        return [x['domain'] for x in resp.json()['results']]

    def add_application_domain(self, app_id, domain):
        """Add a new domain to the specified app ID.

        :param str app_id: the app ID
        :param str domain: the domain name

        :raises api_server.clients.exceptions.ClientError:
        """
        self._request_and_raise(
            'POST', 'v1/apps/{}/domains/'.format(app_id), json={'domain': domain})

    def remove_application_domain(self, app_id, domain):
        """Remove a domain from the specified app ID.

        :param str app_id: the app ID
        :param str domain: the domain name

        :raises api_server.clients.exceptions.ClientError:
        """
        self._request_and_raise(
            'DELETE', 'v1/apps/{}/domains/{}'.format(app_id, domain))

    def run_command(self, app_id, command):
        """Run a one-off command on the host running application
        with specified ID.

        :param str app_id: the app ID
        :param str command: the command to run

        :raises api_server.clients.exceptions.ClientError:
        """
        ret = self._request_and_raise('POST', 'v1/apps/{}/run/'.format(app_id), json={
            'command': command
        }, timeout=None).json()
        return {
            'exit_code': ret[0],
            'output': ret[1],
        }

    def get_application_owner(self, app_id):
        """Get the username of the owner of the specified app ID.

        :param str app_id: the app ID

        :rtype: str
        :returns: the username of the owner

        :raises api_server.clients.exceptions.ClientError:
        """
        resp = self._request_and_raise('GET', 'v1/apps/{}/'.format(app_id))
        return resp.json()['owner']

    def set_application_owner(self, app_id, username):
        """Set the owner of the application to be the specified username.
        Can only be done by someone with admin privilege on this application.

        :param str app_id: the app ID
        :param str username: the username of the new owner

        :raises api_server.clients.exceptions.ClientError:
        """
        self._request_and_raise('POST', 'v1/apps/{}/'.format(app_id), json={
            'owner': username
        })

    def get_application_collaborators(self, app_id):
        """Returns the list of users sharing this application.
        This does NOT include the application owner.

        :param str app_id: the app ID

        :rtype: list
        :returns: The list of usernames of collaborators (str)

        :raises api_server.clients.exceptions.ClientError:
        """
        resp = self._request_and_raise(
            'GET', 'v1/apps/{}/perms/'.format(app_id))
        return resp.json()['users']

    def add_application_collaborator(self, app_id, username):
        """Adds the user with the specified username to the list of
        collaborators

        :param str app_id: the app ID
        :param str username: the username of the collaborator

        :raises api_server.clients.exceptions.ClientError:
        """
        self._request_and_raise('POST', 'v1/apps/{}/perms/'.format(app_id), json={
            'username': username
        })

    def remove_application_collaborator(self, app_id, username):
        """Removes the user with the specified username from the list of
        collaborators

        :param str app_id: the app ID
        :param str username: the username of the collaborator

        :raises api_server.clients.exceptions.ClientError:
        """
        self._request_and_raise(
            'DELETE', 'v1/apps/{}/perms/{}'.format(app_id, username))

    def get_application_log(self, app_id, lines=None):
        """Get the application log.

        :param str app_id: the app ID
        :param int lines: the number of lines of log to return

        :rtype: list
        :returns: list of string, one log entry per line

        :raises api_server.clients.exceptions.ClientError:
        """
        params = {}
        if lines is not None:
            params['log_lines'] = lines
        resp = self._request_and_raise(
            'GET', 'v1/apps/{}/logs/'.format(app_id), params=params)
        logs = resp.json().strip('\n')
        # TODO this doesn't properly handle multi-line logs
        return logs.split('\n')

    def get_keys(self):
        """Get all public keys associated with this user.

        :rtype: dict
        :returns: A dictionary with two keys: 'key_name' and 'key', both str

        :raises api_server.clients.exceptions.ClientError:
        """
        # TODO may have to page
        resp = self._request_and_raise(
            'GET', 'v1/keys/')
        return [{'key_name': x['id'], 'key': x['public']} for x in resp.json()['results']]

    def add_key(self, key_name, key):
        """Add a public key to this user.

        :param str key_name: An ID to be associated with this key
        :param str key: the actual public key

        :raises api_server.clients.exceptions.ClientError:
        """
        self._request_and_raise('POST', 'v1/keys/', json={
            'id': key_name,
            'public': key
        })

    def remove_key(self, key_name):
        """Remove the specified key from this user.

        :param str key_name: The ID associated with this key when added.

        :raises api_server.clients.exceptions.ClientError:
        """
        self._request_and_raise('DELETE', 'v1/keys/{}'.format(key_name))
