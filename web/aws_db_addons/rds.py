import boto3


class RdsNotReadyError(Exception):
    pass


def create_instance(db_instance, engine):
    """Create a new RDS instance for this DB instance.

    :param aws_db_addons.models.DbInstance db_instance:
    :param str engine:

    :raises botocore.exceptions.ClientError:
    """
    rds = boto3.client('rds')
    rds.create_db_instance(
        DBInstanceIdentifier=db_instance.aws_instance_identifier,
        AllocatedStorage=5,
        DBName=db_instance.db_name,
        Engine=engine,
        # General purpose SSD
        StorageType='gp2',

        # can't encrypt t2
        # StorageEncrypted=True,

        AutoMinorVersionUpgrade=True,
        # TODO Set this to true?
        MultiAZ=False,
        MasterUsername=db_instance.master_username,
        MasterUserPassword=db_instance.master_password,
        PubliclyAccessible=True,
        DBInstanceClass='db.t2.micro')


def get_endpoint(db_instance):
    """Get the endpoint for this DB instance. Raises RdsNotReadyError if
    the instance is not ready.

    :param aws_db_addons.models.DbInstance db_instance:
    :param str engine:

    :rtype: str
    :returns: The endpoint (e.g. 'localhost:1234')

    :raises botocore.exceptions.ClientError:
        when there is a client error, including if the instance is not found

    :raises RdsNotReadyError:
    """
    rds = boto3.client('rds')
    instances = rds.describe_db_instances(
        DBInstanceIdentifier=db_instance.aws_instance_identifier)['DBInstances']
    assert len(instances) == 1
    if instances[0]['DBInstanceStatus'] != 'available':
        raise RdsNotReadyError('RDS instance {} is not in the "available" state. The state is "{}".'.format(
            db_instance.aws_instance_identifier, instances[0]['DBInstanceStatus']))
    return '{host}:{port}'.format(
        host=instances[0]['Endpoint']['Address'],
        port=instances[0]['Endpoint']['Port']
    )


def delete_instance(db_instance):
    """Delete the RDS instance corresponding to this DB instance.

    :type aws_db_addons.models.DbInstance db_instance: aws_db_addons.models.DbInstance

    :raises botocore.exceptions.ClientError:
    """
    rds = boto3.client('rds')
    rds.delete_db_instance(
        DBInstanceIdentifier=db_instance.aws_instance_identifier,
        SkipFinalSnapshot=True
    )
