class BaseAddonProvider(object):

    def begin_provision(self, app_id):
        """Kick off the provision process and return a UUID
        for the new addon. This method MUST return immediately.
        In the event of errors, raise any subclass of AddonProviderError.

        @type app_id: str

        @rtype: dict
            A dictionary with the following keys:
            {
                'message': 'the message to be displayed to the user',
                'uuid': 'the unique ID for this addon. Must be a UUID object.',
            }

        @raises: AddonProviderError
            If the resource cannot be allocated.
        """
        raise NotImplementedError

    def provision_complete(self, uuid):
        """Check on the status of provision. This must return
        immediately.

        @type uuid: uuid.UUID

        @rtype: (bool, int)
            The first value should be True if provision is
            complete. The second value is an optional value to
            tell the server how long (in seconds) to wait before
            checking in again. Note that this is only looked at
            if the first value is False

        @raises: AddonProviderError
            If provision failed
        """
        raise NotImplementedError

    def get_config(self, uuid):
        """Get the config necesary to allow the app to use this
        addon's resources.

        @type uuid: uuid.UUID
            The UUID of the addon, returned from `begin_provision`.

        @rtype: dict
            {
                'config': {
                    'ENV_VAR1': ...
                    ...
                }
            }
        @raises: AddonProviderError
            If the config cannot be generated for some reason
            (say, provision never started/failed).
        """
        raise NotImplementedError

    def deprovision(self, uuid):
        """Kicks off the deprovision process. This should return right away.

        @type: uuid: uuid.UUID
            The UUID of the addon

        @rtype: dict
            {
                'message': 'The message to be displayed to the user.'
            }

        @raises: AddonProviderError
            If deprovision cannot start, or if it has already started.
        """
        raise NotImplementedError
