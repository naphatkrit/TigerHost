import pytest

from api_server.addons.event import AddonEvent
from api_server.addons.state import AddonState
from api_server.addons.state_machine_manager import StateMachineManager, StateMachineTransitionError


@pytest.fixture(scope='function')
def manager():
    return StateMachineManager()


@pytest.mark.django_db
def test_transition_success(addon, manager):
    """
    @type addon: api_server.models.Addon
    @type manager: StateMachineManager
    """
    manager.transition_table = {
        AddonState.waiting_for_provision: {
            AddonEvent.provision_success: AddonState.provisioned
        }
    }
    manager.transition(addon, AddonEvent.provision_success)
    assert addon.state == AddonState.provisioned


@pytest.mark.django_db
def test_transition_failure(addon, manager):
    """
    @type addon: api_server.models.Addon
    @type manager: StateMachineManager
    """
    manager.transition_table = {
        AddonState.waiting_for_provision: {
            AddonEvent.provision_success: AddonState.provisioned
        }
    }
    old_state = addon.state
    with pytest.raises(StateMachineTransitionError):
        manager.transition(addon, AddonEvent.deprovision_success)
    assert addon.state == old_state
