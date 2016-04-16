from api_server.clients.base_client import BaseClient


class BaseAuthenticatedClient(BaseClient):
    """The backend client for APIs that require authentication
    """

    def get_all_applications(self):
        """Get all application IDs associated with this user.

        :rtype: list
        :returns: The list of application IDs (str)

        @raises ClientResponseError
        """
        raise NotImplementedError

    def create_application(self, app_id):
        """Create a new application with the specified ID.

        :param str app_id: the app ID

        :raises api_server.clients.exceptions.ClientError:
        """
        raise NotImplementedError

    def delete_application(self, app_id):
        """Delete an application with the specified ID.

        :param str app_id: the app ID

        :raises api_server.clients.exceptions.ClientError:
        """
        raise NotImplementedError

    def set_application_env_variables(self, app_id, bindings):
        """Set the environmental variables for the specified app ID. To unset a variable, set it to ``None``.

        :param str app_id: the app ID
        :param dict bindings: The key-value pair to set in the environment.

        :raises api_server.clients.exceptions.ClientError:
        """
        raise NotImplementedError

    def get_application_env_variables(self, app_id):
        """Get the environmental variables for the specified app ID.

        :param str app_id: the app ID

        :rtype: dict
        :returns: The key-value pair representing the environmental variables

        :raises api_server.clients.exceptions.ClientError:
        """
        raise NotImplementedError

    def get_application_domains(self, app_id):
        """Get all domains associated with the specified app ID.

        :param str app_id: the app ID

        :rtype: list
        :returns: List of domains (str)

        :raises api_server.clients.exceptions.ClientError:
        """
        raise NotImplementedError

    def add_application_domain(self, app_id, domain):
        """Add a new domain to the specified app ID.

        :param str app_id: the app ID
        :param str domain: the domain name

        :raises api_server.clients.exceptions.ClientError:
        """
        raise NotImplementedError

    def remove_application_domain(self, app_id, domain):
        """Remove a domain from the specified app ID.

        :param str app_id: the app ID
        :param str domain: the domain name

        :raises api_server.clients.exceptions.ClientError:
        """
        raise NotImplementedError

    def run_command(self, app_id, command):
        """Run a one-off command on the host running application
        with specified ID.

        :param str app_id: the app ID
        :param str command: the command to run

        :raises api_server.clients.exceptions.ClientError:
        """
        raise NotImplementedError

    def get_application_owner(self, app_id):
        """Get the username of the owner of the specified app ID.

        :param str app_id: the app ID

        :rtype: str
        :returns: the username of the owner

        :raises api_server.clients.exceptions.ClientError:
        """
        raise NotImplementedError

    def set_application_owner(self, app_id, username):
        """Set the owner of the application to be the specified username.
        Can only be done by someone with admin privilege on this application.

        :param str app_id: the app ID
        :param str username: the username of the new owner

        :raises api_server.clients.exceptions.ClientError:
        """
        raise NotImplementedError

    def get_application_collaborators(self, app_id):
        """Returns the list of users sharing this application.
        This does NOT include the application owner.

        :param str app_id: the app ID

        :rtype: list
        :returns: The list of usernames of collaborators (str)

        :raises api_server.clients.exceptions.ClientError:
        """
        raise NotImplementedError

    def add_application_collaborator(self, app_id, username):
        """Adds the user with the specified username to the list of
        collaborators

        :param str app_id: the app ID
        :param str username: the username of the collaborator

        :raises api_server.clients.exceptions.ClientError:
        """
        raise NotImplementedError

    def remove_application_collaborator(self, app_id, username):
        """Removes the user with the specified username from the list of
        collaborators

        :param str app_id: the app ID
        :param str username: the username of the collaborator

        :raises api_server.clients.exceptions.ClientError:
        """
        raise NotImplementedError

    def get_application_log(self, app_id, lines):
        """Get the application log.

        :param str app_id: the app ID
        :param int lines: the number of lines of log to return

        :rtype: list
        :returns: list of string, one log entry per line

        :raises api_server.clients.exceptions.ClientError:
        """
        raise NotImplementedError

    def get_keys(self):
        """Get all public keys associated with this user.

        :rtype: dict
        :returns: A dictionary with two keys: 'key_name' and 'key', both str

        :raises api_server.clients.exceptions.ClientError:
        """
        raise NotImplementedError

    def add_key(self, key_name, key):
        """Add a public key to this user.

        :param str key_name: An ID to be associated with this key
        :param str key: the actual public key

        :raises api_server.clients.exceptions.ClientError:
        """
        raise NotImplementedError

    def remove_key(self, key_name):
        """Remove the specified key from this user.

        :param str key_name: The ID associated with this key when added.

        :raises api_server.clients.exceptions.ClientError:
        """
        raise NotImplementedError
