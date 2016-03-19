import botocore

from api_server.addons.providers.base_provider import BaseAddonProvider
from api_server.addons.providers.exceptions import AddonProviderError
from aws_db_addons import rds
from aws_db_addons.models import DbInstance


class RdsAddonProvider(BaseAddonProvider):

    def __init__(self, engine):
        """Create a new RDS addon provider for the specified engine.

        @type engine: str
            The database engine to use.
            Supported values: mysql, postgres
        """
        self.engine = engine
        self.config_name = 'DATABASE_URL'

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
        instance = DbInstance.objects.create()
        try:
            rds.create_instance(instance, self.engine)
        except botocore.exceptions.ClientError:
            instance.delete()
            raise AddonProviderError('The database cannot be allocated.')
        return {
            'message': 'Database allocated. Please wait a while for it to become available. The URL will be stored at {}.'.format(self.config_name),
            'uuid': instance.uuid,
        }

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
        try:
            instance = DbInstance.objects.get(uuid=uuid)
        except DbInstance.DoesNotExist:
            raise AddonProviderError(
                'Database with uuid {} does not exist.'.format(uuid))
        try:
            rds.get_endpoint(instance)
        except rds.RdsNotReadyError:
            return False, 30
        except botocore.exceptions.ClientError as e:
            raise AddonProviderError(
                'An unexpcted error has occured. {}'.format(e))
        return True, 0

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
        try:
            instance = DbInstance.objects.get(uuid=uuid)
        except DbInstance.DoesNotExist:
            raise AddonProviderError(
                'Database with uuid {} does not exist.'.format(uuid))
        try:
            endpoint = rds.get_endpoint(instance)
        except rds.RdsNotReadyError as e:
            raise AddonProviderError('{}'.format(e))
        except botocore.exceptions.ClientError as e:
            raise AddonProviderError(
                'An unexpcted error has occured. {}'.format(e))
        url = '{protocol}://{username}:{password}@{endpoint}/{db_name}'.format(
            protocol=self.engine,
            username=instance.master_username,
            password=instance.master_password,
            endpoint=endpoint,
            db_name=instance.db_name,
        )
        return {
            'config': {
                self.config_name: url,
            }
        }

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
        try:
            instance = DbInstance.objects.get(uuid=uuid)
        except DbInstance.DoesNotExist:
            raise AddonProviderError(
                'Database with uuid {} does not exist.'.format(uuid))
        try:
            rds.delete_instance(instance)
        except botocore.exceptions.ClientError as e:
            raise AddonProviderError('{}'.format(e))
        return {
            'message': 'Database deleted. Please remove {config_name} manually.'.format(config_name=self.config_name)
        }
