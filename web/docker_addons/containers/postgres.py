from docker_addons.containers.base import BaseContainer


class PostgresContainer(BaseContainer):

    db_name = 'postgresdb'

    def get_environment(self):
        """Get the environment to be created for this container

        :rtype: dict
        :returns: dictionary representing the environment, like {"VAR1": "value1", ...}
        """
        return {
            'POSTGRES_USER': self.container_info.name,
            'POSTGRES_DB': self.db_name,
        }

    def get_image(self):
        """Get the image for this container

        :rtype: str
        :returns: the image name, like postgres:9.5
        """
        return 'postgres:9.5'

    def get_url(self):
        """Return the URL to connect to this container, in the correct protocol

        :rtype: str
        :returns: the URL as a string, like postgres://________
        """
        return 'postgres://{name}@{hostname}:5432/{db}'.format(
            name=self.container_info.name,
            hostname=self.get_docker_hostname(),
            db=self.db_name,
        )
