from docker_addons.containers.base import BaseContainer


class MongoContainer(BaseContainer):

    db_name = 'mongo_db'

    # NOTE: this is not used for security, but is something that is required
    # by the docker image. Security is enforced in the username
    password = 'default'

    def get_environment(self):
        """Get the environment to be created for this container

        :rtype: dict
        :returns: dictionary representing the environment, like {"VAR1": "value1", ...}
        """
        return {
            'MONGODB_PASS': self.password,
            'MONGODB_USER': self.container_info.name,
            'MONGODB_DATABASE': self.db_name,
        }

    def get_image(self):
        """Get the image for this container

        :rtype: str
        :returns: the image name, like postgres:9.5
        """
        return 'tutum/mongodb:3.2'

    def get_url(self):
        """Return the URL to connect to this container, in the correct protocol

        :rtype: str
        :returns: the URL as a string, like postgres://________
        """
        return 'mongodb://{name}:{password}@{hostname}:27017/{db}'.format(
            name=self.container_info.name,
            password=self.password,
            hostname=self.get_docker_hostname(),
            db=self.db_name,
        )
