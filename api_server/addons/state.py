from enum import Enum


class AddonState(Enum):
    waiting_for_provision = 1
    provisioned = 2
    ready = 3
    deprovisioned = 5
    error = 6
    error_should_deprovision = 7


visible_states = [AddonState.waiting_for_provision,
                  AddonState.provisioned, AddonState.ready]
