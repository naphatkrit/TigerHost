from enum import Enum


class AddonEvent(Enum):
    provision_success = 1
    provision_failure = 2

    config_variables_set_success = 3
    config_variables_set_failure = 4

    # NOTE: no failure counterpart because if it fails to start, we won't
    # ever transition (the addon server is most likely temporarily down)
    deprovision_start_success = 5

    deprovision_success = 6
    deprovision_failure = 7
