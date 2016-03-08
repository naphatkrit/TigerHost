from __future__ import absolute_import

import celery
import mock
import pytest

from api_server.addons.event import AddonEvent
from api_server.addons.state import AddonState
from api_server.addons.state_machine_manager import StateMachineManager, StateMachineTransitionError


@pytest.fixture(scope='function')
def manager():
    return StateMachineManager()


@pytest.fixture(scope='function')
def mock_task():
    return mock.Mock(spec=celery.app.task.Task)


@pytest.mark.django_db
def test_transition_helper_success(addon, manager):
    """
    @type addon: api_server.models.Addon
    @type manager: StateMachineManager
    """
    manager.transition_table = {
        AddonState.waiting_for_provision: {
            AddonEvent.provision_success: AddonState.provisioned
        }
    }
    manager._transition_helper(addon, AddonEvent.provision_success)
    assert addon.state == AddonState.provisioned


@pytest.mark.django_db
def test_transition_helper_failure(addon, manager):
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
        manager._transition_helper(addon, AddonEvent.deprovision_success)
    assert addon.state == old_state


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
    with manager.transition(addon.id, AddonEvent.provision_success) as addon_inner:
        addon_inner.provider_name = 'test_provider2'
    addon.refresh_from_db()
    assert addon.state == AddonState.provisioned
    assert addon.provider_name == 'test_provider2'


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
    with pytest.raises(StateMachineTransitionError):
        with manager.transition(addon.id, AddonEvent.deprovision_success) as addon_inner:
            addon_inner.provider_name = 'test_provider2'
    addon.refresh_from_db()
    assert addon.state == AddonState.waiting_for_provision
    assert addon.provider_name == 'test_provider'


@pytest.mark.django_db
def test_start_task(addon, manager, mock_task):
    """
    @type addon: api_server.models.Addon
    @type manager: StateMachineManager
    """
    manager.tasks_table = {
        AddonState.waiting_for_provision: mock_task
    }
    manager.start_task(addon)
    mock_task.delay.assert_called_once_with(addon.id)
