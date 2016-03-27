from enum import Enum

from docker_addons.containers.postgres import PostgresContainer


class AddonTypes(Enum):
    postgres = 1

    def get_container(self, *args, **kwargs):
        """A factory method for creating containers.

        @rtype: docker_addons.containers.base.BaseContainer
        """
        if self is AddonTypes.postgres:
            return PostgresContainer(*args, **kwargs)
        return None
