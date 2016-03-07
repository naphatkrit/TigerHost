from enum import Enum


class AddonState(Enum):
    waiting_for_provision = 1
    provisioned = 2
    ready = 3
    waiting_for_deprovision = 4
    deprovisioned = 5
    error = 6
