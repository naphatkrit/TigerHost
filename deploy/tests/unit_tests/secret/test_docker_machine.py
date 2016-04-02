import mock
import os
import pytest

from tigerhost.utils import contextmanagers

from deploy.secret.docker_machine import store_credentials
from deploy.secret.secret_dir import secret_dir_path
from deploy.utils.path_utils import canonical_path


@pytest.yield_fixture
def fake_credentials_folder():
    with contextmanagers.temp_dir() as temp:
        assert not os.system('touch {}/{}'.format(temp,'ca.pem'))
        assert not os.system('touch {}/{}'.format(temp, 'cert.pem'))
        assert not os.system('touch {}/{}'.format(temp, 'key.pem'))
        yield temp


def test_store_credentials(fake_credentials_folder):
    with mock.patch('subprocess32.check_output') as mocked:
        mocked.return_value = 'export DOCKER_CERT_PATH={}'.format(fake_credentials_folder)
        store_credentials('test_machine')
    mocked.assert_called_once_with(['docker-machine', 'env', 'test_machine'])
    secret_path = canonical_path(secret_dir_path())
    assert os.path.exists(os.path.join(secret_path, 'docker_machines/test_machine', 'ca.pem'))
    assert os.path.exists(os.path.join(secret_path, 'docker_machines/test_machine', 'cert.pem'))
    assert os.path.exists(os.path.join(secret_path, 'docker_machines/test_machine', 'key.pem'))
