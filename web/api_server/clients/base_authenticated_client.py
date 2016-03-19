from api_server.clients.base_client import BaseClient


class BaseAuthenticatedClient(BaseClient):
    """The backend client for API that requires authentication
    """

    def get_all_applications(self):
        """Get all application IDs associated with this user.

        @rtype: list
            The list of application IDs (str)

        @raises ClientResponseError
        """
        raise NotImplementedError

    def create_application(self, app_id):
        """Create a new application with the specified ID.

        @type app_id: str

        @raises ClientResponseError
        """
        raise NotImplementedError

    def delete_application(self, app_id):
        """Delete an application with the specified ID.

        @type app_id: str

        @raises ClientResponseError
        """
        raise NotImplementedError

    def set_application_env_variables(self, app_id, bindings):
        """Set the environmental variables for the specified app ID. To unset a variable, set it to ``None``.

        @type app_id: str

        @type bindings: dict
            The key-value pair to set in the environmental.

        @raises ClientResponseError
        """
        raise NotImplementedError

    def get_application_env_variables(self, app_id):
        """Get the environmental variables for the specified app ID.

        @type app_id: str

        @rtype: dict
            The key-value pair representing the environmental variables

        @raises e: ClientResponseError
        """
        raise NotImplementedError

    def get_application_domains(self, app_id):
        """Get all domains associated with the specified app ID.

        @type app_id: str

        @rtype: list
            List of domains (str)

        @raises e: ClientResponseError
        """
        raise NotImplementedError

    def add_application_domain(self, app_id, domain):
        """Add a new domain to the specified app ID.

        @type app_id: str
        @type domain: str

        @raises e: ClientResponseError
        """
        raise NotImplementedError

    def remove_application_domain(self, app_id, domain):
        """Remove a domain from the specified app ID.

        @type app_id: str
        @type domain: str

        @raises e: ClientResponseError
        """
        raise NotImplementedError

    def run_command(self, app_id, command):
        """Run a one-off command on the host running application
        with specified ID.

        @type app_id: str
        @type command: str

        @raises e: ClientResponseError
        """
        raise NotImplementedError

    def get_application_owner(self, app_id):
        """Get the username of the owner of the specified app ID.

        @type app_id: str

        @rtype: str

        @raises e: ClientResponseError
        """
        raise NotImplementedError

    def set_application_owner(self, app_id, username):
        """Set the owner of the application to be the specified username.
        Can only be done by someone with admin privilege on this application.

        @type app_id: str
        @type username: str

        @raises e: ClientResponseError
        """
        raise NotImplementedError

    def get_application_collaborators(self, app_id):
        """Returns the list of users sharing this application.
        This does NOT include the application owner.

        @type app_id: str

        @rtype: list
            The list of usernames of collaborators (str)

        @raises e: ClientResponseError
        """
        raise NotImplementedError

    def add_application_collaborator(self, app_id, username):
        """Adds the user with the specified username to the list of
        collaborators

        @type app_id: str
        @type username: str

        @raises e: ClientResponseError
        """
        raise NotImplementedError

    def remove_application_collaborator(self, app_id, username):
        """Removes the user with the specified username from the list of
        collaborators

        @type app_id: str
        @type username: str

        @raises e: ClientResponseError
        """
        raise NotImplementedError

    def get_keys(self):
        """Get all public keys associated with this user.

        @rtype: dict
            A dictionary with two keys: 'key_name' and 'key'

        @raises e: ClientResponseError
        """
        raise NotImplementedError

    def add_key(self, key_name, key):
        """Add a public key to this user.

        @type key_name: str
            An ID to be associated with this key

        @type key: str

        @raises e: ClientResponseError
        """
        raise NotImplementedError

    def remove_key(self, key_name):
        """Remove the specified key from this user.

        @type key_name: str
            The ID associated with this key when added.

        @raises e: ClientResponseError
        """
        raise NotImplementedError
