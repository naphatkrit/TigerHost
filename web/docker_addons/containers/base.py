import urlparse


class BaseContainer(object):
    """The base container class. All addon containers
    should subclass this.
    """

    def __init__(self, container_info, docker_client, network_name):
        """Create a new container.
        This does NOT create a container on the docker host

        :param docker_addons.models.ContainerInfo container_info: the container info
        :param docker.Client docker_client: the docker client to use
        :param str network_name: The network to connect new containers to.
        """
        self.container_info = container_info
        self.docker_client = docker_client
        self.network_name = network_name

    def get_environment(self):
        """Get the environment to be created for this container

        :rtype: dict
        :returns: dictionary representing the environment, like {"VAR1": "value1", ...}
        """
        raise NotImplementedError

    def get_image(self):
        """Get the image for this container

        :rtype: str
        :returns: the image name, like postgres:9.5
        """
        raise NotImplementedError

    def get_url(self):
        """Return the URL to connect to this container, in the correct protocol

        :rtype: str
        :returns: the URL as a string, like postgres://________
        """
        raise NotImplementedError

    def get_docker_hostname(self):
        """Return the hostname of the docker host
        associated with the docker client.

        :rtype: str
        :returns: the hostname
        """
        url = urlparse.urlparse(self.docker_client.base_url)
        return url.hostname

    def run_container(self):
        """Connect to the docker host, create a new container, and start it. Save the container ID into container_info.
        """
        # TODO this takes a few seconds because of the pull (20 seconds when
        # the whole image needs to be loaded, 1 second otherwise for me)
        self.docker_client.pull(self.get_image())
        host_config = self.docker_client.create_host_config(
            restart_policy={'Name': 'on-failure', 'MaximumRetryCount': 5},
            network_mode=self.network_name)
        result = self.docker_client.create_container(
            image=self.get_image(),
            environment=self.get_environment(),
            host_config=host_config,
            detach=True,
            name=self.container_info.name,
        )
        self.container_info.container_id = result['Id']
        self.container_info.save()
        self.docker_client.start(self.container_info.container_id)

    def stop_container(self):
        """Stop the container on the docker host
        """
        assert self.container_info.container_id is not None
        self.docker_client.stop(self.container_info.container_id)
