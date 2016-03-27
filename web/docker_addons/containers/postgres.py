from docker_addons.containers.base import BaseContainer


class PostgresContainer(BaseContainer):

    def get_environment(self):
        return {
            'POSTGRES_USER': self.container_info.name
        }

    def get_image(self):
        """Get the image for this container

        @rtype: str
        """
        return 'postgres:9.5'

    def get_url(self):
        """Return the URL to connect to this container, in the correct protocol

        @rtype: str
        """
        return 'postgres://{name}@{hostname}:5432'.format(
            name=self.container_info.name,
            hostname=self.get_docker_hostname(),
        )
