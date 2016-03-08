import mock
import pytest

from api_server.addons.providers.base_provider import BaseAddonProvider
from api_server.addons.providers.exceptions import AddonProviderError
from api_server.addons.state import AddonState
from api_server.addons.tasks import wait_for_provision, wait_for_deprovision, set_config
from api_server.clients.exceptions import ClientError
from api_server.paas_backends import BackendsError


@pytest.fixture(scope='function')
def fake_provider():
    return mock.Mock(spec=BaseAddonProvider)


@pytest.mark.django_db
def test_wait_for_provision_simple(addon, fake_provider):
    """
    @type addon: api_server.models.Addon
    @type fake_provider: mock.Mock
    """
    config = {
        'DATABASE_URL': 'fake://fake',
        'ENV_VAR1': 1,
        'ENV_VAR2': 2.5,
    }
    fake_provider.wait_for_provision.return_value = {
        'config': config
    }
    with mock.patch('api_server.addons.tasks.get_provider_from_provider_name') as mocked:
        mocked.return_value = fake_provider
        result = wait_for_provision.delay(addon.id)
    assert result.get() == addon.id
    addon.refresh_from_db()
    assert addon.state is AddonState.provisioned
    assert addon.config == config
    fake_provider.wait_for_provision.assert_called_once_with(addon.provider_uuid)


@pytest.mark.django_db
def test_wait_for_provision_wrong_state(addon, fake_provider):
    """
    @type addon: api_server.models.Addon
    @type fake_provider: mock.Mock
    """
    addon.state = AddonState.deprovisioned
    addon.save()
    result = wait_for_provision.delay(addon.id)
    assert result.get() == addon.id
    addon.refresh_from_db()
    assert addon.state is AddonState.deprovisioned


@pytest.mark.django_db
def test_wait_for_provision_invalid_config(addon, fake_provider):
    """
    @type addon: api_server.models.Addon
    @type fake_provider: mock.Mock
    """
    config = {
        'DATABASE_URL': 'fake://fake',
        'ENV_VAR1': 1,
        'ENV_VAR2': {},
    }
    fake_provider.wait_for_provision.return_value = {
        'config': config
    }
    with mock.patch('api_server.addons.tasks.get_provider_from_provider_name') as mocked:
        mocked.return_value = fake_provider
        result = wait_for_provision.delay(addon.id)
    assert result.get() == addon.id
    addon.refresh_from_db()
    assert addon.state is AddonState.error
    assert addon.config is None
    fake_provider.wait_for_provision.assert_called_once_with(addon.provider_uuid)


@pytest.mark.django_db
def test_wait_for_provision_missing_config(addon, fake_provider):
    """
    @type addon: api_server.models.Addon
    @type fake_provider: mock.Mock
    """
    fake_provider.wait_for_provision.return_value = {
    }
    with mock.patch('api_server.addons.tasks.get_provider_from_provider_name') as mocked:
        mocked.return_value = fake_provider
        result = wait_for_provision.delay(addon.id)
    assert result.get() == addon.id
    addon.refresh_from_db()
    assert addon.state is AddonState.error
    assert addon.config is None
    fake_provider.wait_for_provision.assert_called_once_with(addon.provider_uuid)


@pytest.mark.django_db
def test_wait_for_provision_wait_failure(addon, fake_provider):
    """
    @type addon: api_server.models.Addon
    @type fake_provider: mock.Mock
    """
    fake_provider.wait_for_provision.side_effect = AddonProviderError
    with mock.patch('api_server.addons.tasks.get_provider_from_provider_name') as mocked:
        mocked.return_value = fake_provider
        result = wait_for_provision.delay(addon.id)
    assert result.get() == addon.id
    addon.refresh_from_db()
    assert addon.state is AddonState.error
    assert addon.config is None
    fake_provider.wait_for_provision.assert_called_once_with(addon.provider_uuid)


@pytest.mark.django_db
def test_wait_for_deprovision_simple(addon, fake_provider):
    """
    @type addon: api_server.models.Addon
    @type fake_provider: mock.Mock
    """
    addon.state = AddonState.waiting_for_deprovision
    addon.save()
    with mock.patch('api_server.addons.tasks.get_provider_from_provider_name') as mocked:
        mocked.return_value = fake_provider
        result = wait_for_deprovision.delay(addon.id)
    assert result.get() == addon.id
    addon.refresh_from_db()
    assert addon.state is AddonState.deprovisioned
    fake_provider.wait_for_deprovision.assert_called_once_with(addon.provider_uuid)


@pytest.mark.django_db
def test_wait_for_deprovision_wrong_state(addon, fake_provider):
    """
    @type addon: api_server.models.Addon
    @type fake_provider: mock.Mock
    """
    addon.state = AddonState.provisioned
    addon.save()
    result = wait_for_deprovision.delay(addon.id)
    assert result.get() == addon.id
    addon.refresh_from_db()
    assert addon.state is AddonState.provisioned


@pytest.mark.django_db
def test_wait_for_deprovision_wait_failure(addon, fake_provider):
    """
    @type addon: api_server.models.Addon
    @type fake_provider: mock.Mock
    """
    addon.state = AddonState.waiting_for_deprovision
    addon.save()
    fake_provider.wait_for_deprovision.side_effect = AddonProviderError
    with mock.patch('api_server.addons.tasks.get_provider_from_provider_name') as mocked:
        mocked.return_value = fake_provider
        result = wait_for_deprovision.delay(addon.id)
    assert result.get() == addon.id
    addon.refresh_from_db()
    assert addon.state is AddonState.error
    fake_provider.wait_for_deprovision.assert_called_once_with(addon.provider_uuid)


@pytest.mark.django_db
def test_set_config_simple(addon, mock_backend_authenticated_client):
    """
    @type addon: api_server.models.Addon
    @type mock_backend_authenticated_client: mock.Mock
    """
    addon.state = AddonState.provisioned
    addon.config = {
        'DATABASE_URL': 'fake://fake',
        'ENV_VAR1': 'var1',
    }
    addon.save()
    with mock.patch('api_server.addons.tasks.get_backend_authenticated_client') as mocked:
        mocked.return_value = mock_backend_authenticated_client
        result = set_config.delay(addon.id)
        mocked.assert_called_once_with(addon.user.username, addon.app.backend)
    assert result.get() == addon.id
    addon.refresh_from_db()
    assert addon.state is AddonState.ready
    mock_backend_authenticated_client.set_application_env_variables.assert_called_once_with(addon.app.app_id, addon.config)


@pytest.mark.django_db
def test_set_config_wrong_state(addon, fake_provider):
    """
    @type addon: api_server.models.Addon
    @type fake_provider: mock.Mock
    """
    addon.state = AddonState.waiting_for_provision
    addon.save()
    result = set_config.delay(addon.id)
    assert result.get() == addon.id
    addon.refresh_from_db()
    assert addon.state is AddonState.waiting_for_provision


@pytest.mark.django_db
def test_set_config_no_app(addon, mock_backend_authenticated_client):
    """
    @type addon: api_server.models.Addon
    @type mock_backend_authenticated_client: mock.Mock
    """
    addon.state = AddonState.provisioned
    addon.config = {
        'DATABASE_URL': 'fake://fake',
        'ENV_VAR1': 'var1',
    }
    addon.app = None
    addon.save()
    with mock.patch('api_server.addons.tasks.get_backend_authenticated_client') as mocked:
        mocked.return_value = mock_backend_authenticated_client
        result = set_config.delay(addon.id)
    assert result.get() == addon.id
    addon.refresh_from_db()
    assert addon.state is AddonState.error


@pytest.mark.django_db
def test_set_config_no_user(addon, mock_backend_authenticated_client):
    """
    @type addon: api_server.models.Addon
    @type mock_backend_authenticated_client: mock.Mock
    """
    addon.state = AddonState.provisioned
    addon.config = {
        'DATABASE_URL': 'fake://fake',
        'ENV_VAR1': 'var1',
    }
    addon.user = None
    addon.save()
    with mock.patch('api_server.addons.tasks.get_backend_authenticated_client') as mocked:
        mocked.return_value = mock_backend_authenticated_client
        result = set_config.delay(addon.id)
    assert result.get() == addon.id
    addon.refresh_from_db()
    assert addon.state is AddonState.error


@pytest.mark.django_db
def test_set_config_no_config(addon, mock_backend_authenticated_client):
    """
    @type addon: api_server.models.Addon
    @type mock_backend_authenticated_client: mock.Mock
    """
    addon.state = AddonState.provisioned
    addon.config = None
    addon.save()
    with mock.patch('api_server.addons.tasks.get_backend_authenticated_client') as mocked:
        mocked.return_value = mock_backend_authenticated_client
        result = set_config.delay(addon.id)
    assert result.get() == addon.id
    addon.refresh_from_db()
    assert addon.state is AddonState.error


@pytest.mark.django_db
def test_set_config_no_backend(addon, mock_backend_authenticated_client):
    """
    @type addon: api_server.models.Addon
    @type mock_backend_authenticated_client: mock.Mock
    """
    addon.state = AddonState.provisioned
    addon.config = {
        'DATABASE_URL': 'fake://fake',
        'ENV_VAR1': 'var1',
    }
    addon.save()
    with mock.patch('api_server.addons.tasks.get_backend_authenticated_client') as mocked:
        mocked.side_effect = BackendsError
        result = set_config.delay(addon.id)
        mocked.assert_called_once_with(addon.user.username, addon.app.backend)
    assert result.get() == addon.id
    addon.refresh_from_db()
    assert addon.state is AddonState.error


@pytest.mark.django_db
def test_set_config_failure(addon, mock_backend_authenticated_client):
    """
    @type addon: api_server.models.Addon
    @type mock_backend_authenticated_client: mock.Mock
    """
    addon.state = AddonState.provisioned
    addon.config = {
        'DATABASE_URL': 'fake://fake',
        'ENV_VAR1': 'var1',
    }
    addon.save()

    mock_backend_authenticated_client.set_application_env_variables.side_effect = ClientError

    with mock.patch('api_server.addons.tasks.get_backend_authenticated_client') as mocked:
        mocked.return_value = mock_backend_authenticated_client
        result = set_config.delay(addon.id)
        mocked.assert_called_once_with(addon.user.username, addon.app.backend)
    assert result.get() == addon.id
    addon.refresh_from_db()
    assert addon.state is AddonState.error
    mock_backend_authenticated_client.set_application_env_variables.assert_called_once_with(addon.app.app_id, addon.config)
