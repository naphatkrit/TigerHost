from django.utils import crypto
from uuid import uuid4

from api_server.addons.providers.base_provider import BaseAddonProvider


class SecretAddonProvider(BaseAddonProvider):
    """The secret addon. This generates a cryptographically secure symmetric
    key and store it in the environmental variable SECRET_KEY"""

    config_name = 'SECRET_KEY'

    def _get_config_name(self, config_customization=None):
        if config_customization is None:
            return self.config_name
        return config_customization + '_' + self.config_name

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
        return {
            'message': 'A secret key will be stored into {} or {}.'.format(self.config_name, self._get_config_name('<CUSTOM_NAME>')),
            'uuid': uuid4(),
        }

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
        return True, 0

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
        return {
            'config': {
                self._get_config_name(config_customization=config_customization): crypto.get_random_string(length=100)
            }
        }

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
        return {
            'message': 'Please remove {} or {} from your config manually.'.format(self.config_name, self._get_config_name('<CUSTOM_NAME>'))
        }
