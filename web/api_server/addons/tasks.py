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

    :rtype: bool
    :returns: True iff valid
    """
    for k, v in config.iteritems():
        if not isinstance(k, basestring):
            return False
        if not isinstance(v, basestring) and type(v) not in [int, float]:
            return False
    return True


# NOTE: all tasks MUST return the same ID back out, so they can be chained


@app.task(bind=True, max_retries=None)
def check_provision(self, addon_id):
    """A task that checks if provision is complete
    """
    try:
        addon = Addon.objects.get(pk=addon_id)
    except Addon.DoesNotExist:
        # TODO log?
        raise
    if addon.state is not AddonState.waiting_for_provision:
        # TODO log?
        return addon_id
    manager = StateMachineManager()
    try:
        provider = get_provider_from_provider_name(addon.provider_name)
    except AddonProviderError:
        # TODO log?
        # transition so this task doesn't get restarted needlessly
        with manager.transition(addon_id, AddonEvent.provision_failure):
            pass
        raise

    # check if provision is done
    try:
        ready, delay = provider.provision_complete(addon.provider_uuid)
    except AddonProviderError:
        with manager.transition(addon_id, AddonEvent.provision_failure):
            pass
        return addon_id
    if not ready:
        raise self.retry(countdown=delay)

    # provision is done, store result
    try:
        result = provider.get_config(addon.provider_uuid, config_customization=addon.config_customization)
    except AddonProviderError:
        with manager.transition(addon_id, AddonEvent.provision_failure):
            pass
        return addon_id

    if 'config' not in result or not _valid_config(result['config']):
        with manager.transition(addon_id, AddonEvent.provision_failure):
            pass
    else:
        with manager.transition(addon_id, AddonEvent.provision_success) as addon:
            addon.config = result['config']
    return addon_id


@app.task
def deprovision(addon_id):
    """A task that kicks off the deprovision process
    """
    try:
        addon = Addon.objects.get(pk=addon_id)
    except Addon.DoesNotExist:
        # TODO log?
        raise

    manager = StateMachineManager()
    try:
        provider = get_provider_from_provider_name(addon.provider_name)
    except AddonProviderError:
        # TODO log?
        # transition so this task doesn't get restarted needlessly
        with manager.transition(addon_id, AddonEvent.deprovision_failure):
            pass
        raise

    try:
        provider.deprovision(addon.provider_uuid)
    except AddonProviderError:
        # TODO retry?
        with manager.transition(addon_id, AddonEvent.deprovision_failure):
            pass
        return addon_id
    with manager.transition(addon_id, AddonEvent.deprovision_success):
        pass
    return addon_id


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
        return addon_id

    if not addon.app or not addon.user or addon.config is None:
        # TODO log?
        with manager.transition(addon_id, AddonEvent.config_variables_set_failure):
            pass
        return addon_id

    try:
        backend_client = get_backend_authenticated_client(
            addon.user.username, addon.app.backend)
    except BackendsError:
        # TODO log?
        with manager.transition(addon_id, AddonEvent.config_variables_set_failure):
            pass
        return addon_id

    try:
        backend_client.set_application_env_variables(
            addon.app.app_id, addon.config)
    except ClientError:
        # TODO retriable
        # TODO log?
        with manager.transition(addon_id, AddonEvent.config_variables_set_failure):
            pass
        return addon_id

    with manager.transition(addon_id, AddonEvent.config_variables_set_success):
        pass
    return addon_id
