from enum import Enum

from docker_addons.containers.mongo import MongoContainer
from docker_addons.containers.postgres import PostgresContainer


class AddonTypes(Enum):
    postgres = 1
    mongo = 2

    def get_container(self, *args, **kwargs):
        """A factory method for creating containers.

        :rtype: docker_addons.containers.base.BaseContainer
        """
        if self is AddonTypes.postgres:
            return PostgresContainer(*args, **kwargs)
        elif self is AddonTypes.mongo:
            return MongoContainer(*args, **kwargs)
        return None
