import docker
import os

from django.conf import settings


def create_client():
    """Create a new Docker client from the settings.

    :rtype: docker.Client
    """
    tls_config = docker.tls.TLSConfig(
        client_cert=(os.path.join(settings.DOCKER_CERT_PATH, 'cert.pem'),
                     os.path.join(settings.DOCKER_CERT_PATH, 'key.pem')),
        ca_cert=os.path.join(settings.DOCKER_CERT_PATH, 'ca.pem'),
        verify=True,
        assert_hostname=False,  # TODO this should probably be True
    )
    return docker.Client(base_url=settings.DOCKER_HOST, tls=tls_config)
