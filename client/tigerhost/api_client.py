import requests
import urlparse

from wsse import WSSEAuth


class ApiClientResponseError(Exception):
    """Represents an error in communicating with the server
    """

    def __init__(self, response):
        """Create a new :code:`ApiClientResponseError`.

        :param requests.Response response:
        the response object returned from the errorneous request
        """
        self.response = response

    def __unicode__(self):
        return """Response Code {code}

        {body}
        """.format(code=self.response.status_code, body=self.response.text)

    def __str__(self):
        return self.__unicode__().encode('utf-8')


class ApiClientAuthenticationError(ApiClientResponseError):
    pass


class ApiClient(object):

    def __init__(self, api_server_url, username, api_key):
        """Create a new :code:`ApiClient`.

        :param str api_server_url:
        :param str username:
        :param str api_key:
        """
        self.api_server_url = api_server_url
        self.username = username
        self.api_key = api_key

    def _request_and_raise(self, method, path, **kwargs):
        """Sends a request to the api server.

        :param str method: HTTP method, such as "POST", "GET", "PUT"
        :param str path: The extra http path to be appended to the deis URL

        :rtype: requests.Response

        :raises tigerhost.api_client.ApiClientAuthenticationError:
            if the response status code is 401

        :raises tigerhost.api_client.ApiClientResponseError:
            if the response status code is not 401 and not in the [200, 300) range.
        """
        resp = requests.request(method, urlparse.urljoin(
            self.api_server_url, path), auth=WSSEAuth(self.username, self.api_key), **kwargs)

        if resp.status_code == 401:
            raise ApiClientAuthenticationError(resp)
        if not 200 <= resp.status_code < 300:
            raise ApiClientResponseError(resp)
        return resp

    def test_api_key(self):
        """Hit the test end point for API key

        :raises tigerhost.api_client.ApiClientAuthenticationError:
        :raises tigerhost.api_client.ApiClientResponseError:
        """
        self._request_and_raise('GET', 'api/test_api_key/')

    def get_backends(self):
        """Get the backends that this user has access to.

        :rtype: dict
        :returns: dictionary with the following format:{

                'backends': ['backend1', 'backend2', ...]

                'default': 'backend1'
            }
        """
        resp = self._request_and_raise('GET', 'api/v1/backends/')
        return resp.json()

    def create_application(self, app_id, backend=None):
        """Create a new application with the specified ID.

        :param str app_id:
        :param str backend:

        :raises tigerhost.api_client.ApiClientResponseError:
        """
        body = {
            'id': app_id
        }
        if backend is not None:
            body['backend'] = backend
        self._request_and_raise('POST', 'api/v1/apps/', json=body)

    def delete_application(self, app_id):
        """Delete an application with the specified ID.

        :param str app_id:

        :raises tigerhost.api_client.ApiClientResponseError:
        """
        self._request_and_raise('DELETE', 'api/v1/apps/{}/'.format(app_id))

    def get_all_applications(self):
        """Get all application IDs associated with this user.

        :rtype: dict
        :returns: dict with format: {
            'backend1': ['app1', ...],

            'backend2': ['app1', ...],

            ...
        }
        """
        resp = self._request_and_raise('GET', 'api/v1/apps/')
        return resp.json()

    def set_application_env_variables(self, app_id, bindings):
        """Set the environmental variables for the specified app ID. To unset a variable, set it to ``None``.

        :param str app_id:

        :param dict bindings:
            The key-value pair to set in the environmental. ``None`` value = unset.

        :raises tigerhost.api_client.ApiClientResponseError:
        """
        self._request_and_raise(
            'POST', 'api/v1/apps/{}/env/'.format(app_id), json=bindings)

    def get_application_env_variables(self, app_id):
        """Get the environmental variables for the specified app ID.

        :param str app_id:

        :rtype: dict
        :returns: The key-value pair representing the environmental variables

        :raises tigerhost.api_client.ApiClientResponseError:
        """
        resp = self._request_and_raise(
            'GET', 'api/v1/apps/{}/env/'.format(app_id))
        return resp.json()

    def get_application_domains(self, app_id):
        """Get all domains associated with the specified app ID.

        :param str app_id:

        :rtype: list
        :returns: List of domains (str)

        :raises tigerhost.api_client.ApiClientResponseError:
        """
        resp = self._request_and_raise(
            'GET', 'api/v1/apps/{}/domains/'.format(app_id))
        return resp.json()['results']

    def add_application_domain(self, app_id, domain):
        """Add a new domain to the specified app ID.

        :param str app_id:
        :param str domain:

        :raises tigerhost.api_client.ApiClientResponseError:
        """
        self._request_and_raise(
            'POST', 'api/v1/apps/{}/domains/'.format(app_id), json={'domain': domain})

    def remove_application_domain(self, app_id, domain):
        """Remove a domain from the specified app ID.

        :param str app_id:
        :param str domain:

        :raises tigerhost.api_client.ApiClientResponseError:
        """
        self._request_and_raise(
            'DELETE', 'api/v1/apps/{}/domains/{}/'.format(app_id, domain))

    def run_command(self, app_id, command):
        """Run a one-off command for this application.

        :param str app_id:
        :param str command:

        :rtype: dict
        :returns: a dictionary with keys 'exit_code' and 'output'

        :raises tigerhost.api_client.ApiClientResponseError:
        """
        resp = self._request_and_raise('POST', 'api/v1/apps/{}/run/'.format(app_id), json={
            'command': command
        }, timeout=None)
        return resp.json()

    def get_application_git_remote(self, app_id):
        """Get the git remote for the specified app ID.

        :param str app_id:

        :rtype: str

        :raises tigerhost.api_client.ApiClientResponseError:
        """
        resp = self._request_and_raise('GET', 'api/v1/apps/{}/'.format(app_id))
        return resp.json()['remote']

    def get_application_owner(self, app_id):
        """Get the username of the owner of the specified app ID.

        :param str app_id:

        :rtype: str

        :raises tigerhost.api_client.ApiClientResponseError:
        """
        resp = self._request_and_raise('GET', 'api/v1/apps/{}/'.format(app_id))
        return resp.json()['owner']

    def set_application_owner(self, app_id, username):
        """Set the owner of the application to be the specified username.
        Can only be done by someone with admin privilege on this application.

        :param str app_id:
        :param str username:

        :raises tigerhost.api_client.ApiClientResponseError:
        """
        self._request_and_raise('POST', 'api/v1/apps/{}/'.format(app_id), json={
            'owner': username
        })

    def get_application_collaborators(self, app_id):
        """Returns the list of users sharing this application.
        This does NOT include the application owner.

        :param str app_id:

        :rtype: list
        :returns: The list of usernames of collaborators (str)

        :raises tigerhost.api_client.ApiClientResponseError:
        """
        resp = self._request_and_raise(
            'GET', 'api/v1/apps/{}/collaborators/'.format(app_id))
        return resp.json()['results']

    def add_application_collaborator(self, app_id, username):
        """Adds the user with the specified username to the list of
        collaborators

        :param str app_id:
        :param str username:

        :raises tigerhost.api_client.ApiClientResponseError:
        """
        self._request_and_raise('POST', 'api/v1/apps/{}/collaborators/'.format(app_id), json={
            'username': username
        })

    def remove_application_collaborator(self, app_id, username):
        """Removes the user with the specified username from the list of
        collaborators

        :param str app_id:
        :param str username:

        :raises tigerhost.api_client.ApiClientResponseError:
        """
        self._request_and_raise(
            'DELETE', 'api/v1/apps/{}/collaborators/{}/'.format(app_id, username))

    def get_application_addons(self, app_id):
        """Returns all addons installed for this app.

        :param str app_id:

        :rtype: list
        :returns: list of dictionary with keys 'provider_name', 'display_name', and 'status'

        :raises tigerhost.api_client.ApiClientResponseError:
        """
        resp = self._request_and_raise(
            'GET', 'api/v1/apps/{}/addons/'.format(app_id))
        return resp.json()['results']

    def get_application_addon(self, app_id, addon_name):
        """Return a specific addon installed for this app.

        :param str app_id:
        :param str addon_name:

        :rtype: dict
        :returns: same as the return type for ``get_application_addons``

        :raises tigerhost.api_client.ApiClientResponseError:
        """
        resp = self._request_and_raise(
            'GET', 'api/v1/apps/{}/addons/{}/'.format(app_id, addon_name))
        return resp.json()

    def create_application_addon(self, app_id, addon, config_customization=None):
        """Create a new addon for this app.

        :param str app_id:
        :param str addon:
        :param str config_customization:

        :rtype: dict
        :returns: dict with keys 'message' and 'addon'.
            'addon' contains a dictionary representation of the created addon.

        :raises tigerhost.api_client.ApiClientResponseError:
        """
        data = {
            'provider_name': addon
        }
        if config_customization is not None:
            data['config_customization'] = config_customization
        resp = self._request_and_raise(
            'POST', 'api/v1/apps/{}/addons/'.format(app_id), json=data)
        return resp.json()

    def delete_application_addon(self, app_id, addon_name):
        """Delete the addon from this app.

        :param str app_id:
        :param str addon:

        :rtype: dict
        :returns: dict with keys 'message'

        :raises tigerhost.api_client.ApiClientResponseError:
        """
        resp = self._request_and_raise(
            'DELETE', 'api/v1/apps/{}/addons/{}/'.format(app_id, addon_name))
        return resp.json()

    def get_application_logs(self, app_id, lines=None):
        """Get the application log

        :param str app_id:
        :param int lines: the number of log entries to return

        :rtype: list
        :returns: list of dictionary with the following keys:{

            'process': 'run.1',

            'message': 'sample message',

            'app': 'sample-python',

            'timestamp': '2016-04-16T14:26:03UTC',

        }

        :raises tigerhost.api_client.ApiClientResponseError:
        """
        params = {}
        if lines is not None:
            params['lines'] = lines
        resp = self._request_and_raise(
            'GET', 'api/v1/apps/{}/logs/'.format(app_id), params=params)
        return resp.json()['results']

    def get_keys(self):
        """Get all public keys associated with this user.

        :rtype: dict
        :returns: dictionary with format: {

            'backend1': [{

                            "key_name": "my_key_name",

                            "key": "ssh-rsa ..."

                            }, ...],

            'backend2': [...],

            ...
        }

        :raises tigerhost.api_client.ApiClientResponseError:
        """
        resp = self._request_and_raise(
            'GET', 'api/v1/keys/')
        return resp.json()

    def add_key(self, key_name, key, backend=None):
        """Add a public key to this user.

        :param str key_name: An ID to be associated with this key
        :param str key:
        :param str backend:

        :raises tigerhost.api_client.ApiClientResponseError:
        """
        body = {
            'key_name': key_name,
            'key': key,
        }
        if backend is not None:
            body['backend'] = backend
        self._request_and_raise('POST', 'api/v1/keys/', json=body)

    def remove_key(self, key_name, backend):
        """Remove the specified key from this user.

        :param str key_name: The ID associated with this key when added.
        :param str backend:

        :raises tigerhost.api_client.ApiClientResponseError:
        """
        self._request_and_raise(
            'DELETE', 'api/v1/keys/{}/{}/'.format(backend, key_name))
