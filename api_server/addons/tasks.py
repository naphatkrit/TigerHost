from api_server.addons.event import AddonEvent
from api_server.addons.providers.exceptions import AddonProviderError
from api_server.addons.providers.utils import get_provider_from_provider_name
from api_server.addons.state import AddonState
from api_server.addons.state_machine_manager import StateMachineManager
from api_server.celery import app
from api_server.clients.exceptions import ClientError
from api_server.models import Addon
from api_server.paas_backends import get_backend_authenticated_client, BackendsError


def _valid_config(config):
    """Check if the config is valid. Valid config has a string
    for keys and a string, int, or float for values.

    @rtype: bool
        True iff valid
    """
    for k, v in config.iteritems():
        if not isinstance(k, basestring):
            return False
        if not isinstance(v, basestring) and type(v) not in [int, float]:
            return False
    return True


@app.task
def wait_for_provision(addon_id):
    """A task that waits for provision to complete."""
    # TODO switch to a model that doesn't block but simply retries
    try:
        addon = Addon.objects.get(pk=addon_id)
    except Addon.DoesNotExist:
        # TODO log?
        raise
    if addon.state is not AddonState.waiting_for_provision:
        # TODO log?
        return
    try:
        provider = get_provider_from_provider_name(addon.provider_name)
    except AddonProviderError:
        # TODO log?
        # TODO transition? this looks like a recoverable error
        raise

    manager = StateMachineManager()
    try:
        result = provider.wait_for_provision(addon.provider_uuid)
    except AddonProviderError:
        with manager.transition(addon_id, AddonEvent.provision_failure):
            pass
        return

    if 'config' not in result or not _valid_config(result['config']):
        with manager.transition(addon_id, AddonEvent.provision_failure):
            pass
    else:
        with manager.transition(addon_id, AddonEvent.provision_success) as addon:
            addon.config = result['config']
    # TODO should start a new task if needed


@app.task
def wait_for_deprovision(addon_id):
    """A task that waits for deprovision to complete."""
    try:
        addon = Addon.objects.get(pk=addon_id)
    except Addon.DoesNotExist:
        # TODO log?
        raise
    if addon.state is not AddonState.waiting_for_deprovision:
        # TODO log?
        return
    try:
        provider = get_provider_from_provider_name(addon.provider_name)
    except AddonProviderError:
        # TODO log?
        # TODO transition? this looks like a recoverable error
        raise

    manager = StateMachineManager()
    try:
        provider.wait_for_deprovision(addon.provider_uuid)
    except AddonProviderError:
        with manager.transition(addon_id, AddonEvent.deprovision_failure):
            pass
        return
    with manager.transition(addon_id, AddonEvent.deprovision_success):
        pass
    # TODO should start a new task if needed


@app.task
def set_config(addon_id):
    """The addon has been provisioned. Now set the config"""
    try:
        addon = Addon.objects.get(pk=addon_id)
    except Addon.DoesNotExist:
        # TODO log?
        raise

    manager = StateMachineManager()

    if addon.state is not AddonState.provisioned:
        # TODO log?
        return

    if not addon.app or not addon.user or addon.config is None:
        # TODO log?
        # TODO this is different from provision failure. We do want to clean up
        with manager.transition(addon_id, AddonEvent.config_variables_set_failure):
            pass
        return

    try:
        backend_client = get_backend_authenticated_client(
            addon.user.username, addon.app.backend)
    except BackendsError:
        # TODO log?
        # TODO this is different from provision failure. We do want to clean up
        with manager.transition(addon_id, AddonEvent.config_variables_set_failure):
            pass
        return

    try:
        backend_client.set_application_env_variables(addon.app.app_id, addon.config)
    except ClientError:
        # TODO retriable
        # TODO log?
        # TODO this is different from provision failure. We do want to clean up
        with manager.transition(addon_id, AddonEvent.config_variables_set_failure):
            pass
        return

    with manager.transition(addon_id, AddonEvent.config_variables_set_success):
        pass
    # TODO should start a new task if needed
