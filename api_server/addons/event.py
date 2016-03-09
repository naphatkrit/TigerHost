from enum import Enum


class AddonEvent(Enum):
    provision_success = 1
    provision_failure = 2

    config_variables_set_success = 3
    config_variables_set_failure = 4

    deprovision_success = 6
    deprovision_failure = 7
