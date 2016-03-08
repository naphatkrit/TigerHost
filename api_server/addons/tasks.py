from api_server.addons.event import AddonEvent
from api_server.addons.providers.exceptions import AddonProviderError
from api_server.addons.providers.utils import get_provider_from_provider_name
from api_server.addons.state import AddonState
from api_server.addons.state_machine_manager import StateMachineManager
from api_server.celery import app
from api_server.models import Addon


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
