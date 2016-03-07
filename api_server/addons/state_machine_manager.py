from api_server.addons.event import AddonEvent
from api_server.addons.state import AddonState


class StateMachineError(Exception):
    pass


class StateMachineTransitionError(Exception):
    pass


class StateMachineManager(object):

    transition_table = {
        AddonState.waiting_for_provision: {
            AddonEvent.provision_success: AddonState.provisioned,
            AddonEvent.provision_failure: AddonState.error,
        },
        AddonState.provisioned: {
            AddonEvent.config_variables_set_success: AddonState.ready,
            AddonEvent.config_variables_set_failure: AddonState.error,
        },
        AddonState.ready: {
            AddonEvent.deprovision_start_success: AddonState.waiting_for_deprovision,
        },
        AddonState.waiting_for_deprovision: {
            AddonEvent.deprovision_success: AddonState.deprovisioned,
            AddonEvent.deprovision_failure: AddonState.error,
        },
    }

    def transition(self, addon, event):
        """Transition to a different state. Doesn't actually save.

        @type addon: api_server.models.Addon
        @type event: AddonEvent

        @raises: StateMachineTransitionError
        """
        # can't handle atomicity here, because we may want to save some things
        # in addition to the new state
        try:
            final_state = self.transition_table[addon.state][event]
        except KeyError:
            raise StateMachineTransitionError(
                'Invalid transition for state {} with event {}.'.format(addon.state.name, event.name))
        addon.state = final_state
