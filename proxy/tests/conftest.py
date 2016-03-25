import pytest

from twisted.test import proto_helpers


pytest_plugins = "pytest_twisted"


@pytest.fixture(scope='function')
def fake_transport():
    return proto_helpers.StringTransport()
