class BaseAddonProvider(object):
    """The base class for all addon providers."""

    def begin_provision(self, app_id):
        """Kick off the provision process and return a UUID
        for the new addon. This method MUST return immediately.
        In the event of errors, raise any subclass of
        :py:obj:`AddonProviderError <api_server.addons.providers.exceptions.AddonProviderError>`.

        :param str app_id: the ID of the app that this addon will be for

        :rtype: dict
        :return: A dictionary with the following keys:\{

                'message': 'the message to be displayed to the user',

                'uuid': 'the unique ID for this addon. Must be a UUID object.',
            }

        :raises api_server.addons.providers.exceptions.AddonProviderError: If the resource cannot be allocated.
        """
        raise NotImplementedError

    def provision_complete(self, uuid):
        """Check on the status of provision. This must return
        immediately.

        :param uuid.UUID uuid: The UUID returned from :py:meth:`begin_provision`

        :rtype: tuple
        :return: (bool, int) - The first value should be True if provision is
            complete. The second value is an optional value to
            tell the server how long (in seconds) to wait before
            checking in again. Note that this is only looked at
            if the first value is False

        :raises api_server.addons.providers.exceptions.AddonProviderError: If provision failed.
        """
        raise NotImplementedError

    def get_config(self, uuid, config_customization=None):
        """Get the config necesary to allow the app to use this
        addon's resources.

        :param uuid.UUID uuid: The UUID returned from :py:meth:`begin_provision`
        :param str config_customization: A string used to avoid conflict in config
        variable names. This string should be incorporated into each of the config
        variable names somehow, for example, <custom_name>_DATABASE_URL.

        :rtype: dict
        :return: A dictionary with the following keys:\{

                'config':\{

                    'ENV_VAR1': ...

                    ...
                }
            }
        :raises api_server.addons.providers.exceptions.AddonProviderError:
            If the config cannot be generated for some reason
            (say, provision never started/failed).
        """
        raise NotImplementedError

    def deprovision(self, uuid):
        """Kicks off the deprovision process. This should return right away.

        :param uuid.UUID uuid: The UUID returned from :py:meth:`begin_provision`

        :rtype: dict
        :return: A dictionary with the following keys:\{

                'message': 'The message to be displayed to the user.'
            }

        :raises api_server.addons.providers.exceptions.AddonProviderError:
            If deprovision cannot start, or if it has already started.
        """
        raise NotImplementedError
