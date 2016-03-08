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

    def wait_for_provision(self, uuid):
        """This method should only return after the provision process
        has ended. In the event that the provision process has already
        completed, just return immediately. That is, this method should
        not assume that it will only be called when provision is taking
        place. As long as the resource is still available, this method
        should work properly. If the resource is no longer available,
        raise AddonProviderInvalidOperationError

        @type uuid: uuid.UUID
            The UUID of the addon, returned from `begin_provision`.

        @rtype: dict
            {
                'config': {
                    'ENV_VAR1': ...
                    ...
                }
            }

        @raises: AddonProviderInvalidOperationError
            If the resource is no longer available, or if the provision
            fails.
        """
        raise NotImplementedError

    def begin_deprovision(self, uuid):
        """Kicks off the deprovision process. If that cannot be completed,
        raise any subclass of AddonProviderError

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

    def wait_for_deprovision(self, uuid):
        """Only return when deprovision is complete.

        @type: uuid: uuid.UUID
        """
        raise NotImplementedError
