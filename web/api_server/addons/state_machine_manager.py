from contextlib import contextmanager
from django.db import transaction

from api_server.addons.event import AddonEvent
from api_server.addons.state import AddonState
from api_server.celery import app
from api_server.models import Addon


class StateMachineError(Exception):
    pass


class StateMachineTransitionError(Exception):
    pass


@app.task
def _continue_state_machine(addon_id):
    state_machine_manager = StateMachineManager()
    state_machine_manager.start_task(addon_id)


class StateMachineManager(object):

    def __init__(self):
        from api_server.addons.tasks import check_provision, set_config, deprovision
        self.transition_table = {
            AddonState.waiting_for_provision: {
                AddonEvent.provision_success: AddonState.provisioned,
                AddonEvent.provision_failure: AddonState.error,
                AddonEvent.deprovision_success: AddonState.deprovisioned,
            },
            AddonState.provisioned: {
                AddonEvent.config_variables_set_success: AddonState.ready,
                AddonEvent.config_variables_set_failure: AddonState.error_should_deprovision,
                AddonEvent.deprovision_success: AddonState.deprovisioned,
            },
            AddonState.ready: {
                AddonEvent.deprovision_success: AddonState.deprovisioned,
                AddonEvent.deprovision_failure: AddonState.error,
            },
            AddonState.error_should_deprovision: {
                AddonEvent.deprovision_success: AddonState.error,
                AddonEvent.deprovision_failure: AddonState.error,
            },
        }

        self.tasks_table = {
            AddonState.waiting_for_provision: check_provision,
            AddonState.provisioned: set_config,
            AddonState.error_should_deprovision: deprovision,
        }

    def _transition_helper(self, addon, event):
        """Transition to a different state. Doesn't actually save.

        @type addon: api_server.models.Addon
        @type event: AddonEvent

        @raises: StateMachineTransitionError
        """
        try:
            final_state = self.transition_table[addon.state][event]
        except KeyError:
            raise StateMachineTransitionError(
                'Invalid transition for state {} with event {}.'.format(addon.state.name, event.name))
        addon.state = final_state

    @contextmanager
    def transition(self, addon_id, event):
        """A context manager for transitioning to a different state.

        The Addon is locked with select_for_update() and
        yielded. Upon returning, the transition is performed,
        and the Addon is saved. If an exception was raised,
        everything is rolled back.

        If the transition is  invalid, the yield still
        happens, but the result will be rolled back.

        @type addon_id: int
        @type event: AddonEvent

        @raises: StateMachineTransitionError
        @raises: Addon.DoesNotExist
        @raises: Exception
            Whatever was raised in the with block does not
            get caught.
        """
        with transaction.atomic():
            addon = Addon.objects.select_for_update().get(pk=addon_id)
            yield addon
            self._transition_helper(addon, event)
            addon.save()

    def start_task(self, addon_id):
        """Kick off a task for this addon, if necessary.

        Uses the tasks table.

        @type: addon: api_server.models.Addon
        """
        addon = Addon.objects.get(pk=addon_id)
        if addon.state in self.tasks_table:
            self.tasks_table[addon.state].apply_async((addon.id,), link=_continue_state_machine.s())
