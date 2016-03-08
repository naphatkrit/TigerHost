import pytest
import uuid

from api_server.addons.state import AddonState
from api_server.models import Addon


@pytest.fixture(scope='function')
def addon(make_app, user):
    return Addon.objects.create(
        provider_name='test_provider', provider_uuid=uuid.uuid4(), app=make_app, state=AddonState.waiting_for_provision, user=user)
