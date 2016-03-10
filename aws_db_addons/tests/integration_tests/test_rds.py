import botocore
import pytest

from aws_db_addons.models import DbInstance
from aws_db_addons.rds import create_instance, get_endpoint, delete_instance, RdsNotReadyError


@pytest.mark.django_db
def test_rds():
    db_instance = DbInstance.objects.create()
    with pytest.raises(botocore.exceptions.ClientError):
        get_endpoint(db_instance)
    create_instance(db_instance, 'postgres')
    with pytest.raises(RdsNotReadyError):
        get_endpoint(db_instance)
    delete_instance(db_instance)
