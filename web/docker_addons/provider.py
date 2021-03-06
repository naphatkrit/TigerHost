import docker

from api_server.addons.providers.base_provider import BaseAddonProvider
from api_server.addons.providers.exceptions import AddonProviderError
from django.conf import settings

from docker_addons.docker_client import create_client
from docker_addons.models import ContainerInfo


class DockerAddonProvider(BaseAddonProvider):

    def __init__(self, container_type, config_name):
        """Create a new Docker addon provider for
        the specified container type.

        :param docker_addons.containers.types.AddonTypes container_type: the addon type
        :param str config_name: the name of the config to store in
        """
        self.config_name = config_name
        self.docker_client = create_client()
        self.container_type = container_type

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
        instance = ContainerInfo.objects.create()
        container = self.container_type.get_container(
            container_info=instance,
            docker_client=self.docker_client,
            network_name=settings.DOCKER_NETWORK,
        )
        try:
            container.run_container()
        except (docker.errors.APIError, docker.errors.DockerException):
            raise AddonProviderError('Addon cannot be allocated.')
        return {
            'message': 'Addon allocated. Please wait a while for it to become available. The URL will be stored at {} or {}.'.format(self.config_name, self._get_config_name('<CUSTOM_NAME>')),
            'uuid': instance.uuid,
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
        try:
            instance = ContainerInfo.objects.get(uuid=uuid)
        except ContainerInfo.DoesNotExist:
            raise AddonProviderError(
                'Addon with uuid {} does not exist.'.format(uuid))
        container = self.container_type.get_container(
            container_info=instance,
            docker_client=self.docker_client,
            network_name=settings.DOCKER_NETWORK,
        )
        return {
            'config': {
                self._get_config_name(config_customization=config_customization): container.get_url(),
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
        try:
            instance = ContainerInfo.objects.get(uuid=uuid)
        except ContainerInfo.DoesNotExist:
            raise AddonProviderError(
                'Addon with uuid {} does not exist.'.format(uuid))
        container = self.container_type.get_container(
            container_info=instance,
            docker_client=self.docker_client,
            network_name=settings.DOCKER_NETWORK,
        )
        try:
            container.stop_container()
        except (docker.errors.APIError, docker.errors.DockerException) as e:
            raise AddonProviderError('{}'.format(e))
        return {
            'message': 'Addon deleted. PPlease remove {config_name} or {custom_name} manually.'.format(
                config_name=self.config_name,
                custom_name=self._get_config_name('<CUSTOM_NAME>'))
        }
