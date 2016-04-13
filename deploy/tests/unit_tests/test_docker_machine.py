import mock
import os
import pytest

from tigerhost.utils import contextmanagers

from deploy.docker_machine import check_call, check_output, retrieve_credentials, docker_machine_storage_path, MachineNotFoundError, get_url


@pytest.fixture
def fake_machine_name():
    return 'test_machine'


@pytest.fixture(scope='function')
def fake_machine_credentials(fake_machine_name):
    path = os.path.join(docker_machine_storage_path(), 'machines', fake_machine_name)
    os.makedirs(path)
    assert not os.system('touch {}/{}'.format(path, 'ca.pem'))
    assert not os.system('touch {}/{}'.format(path, 'cert.pem'))
    assert not os.system('touch {}/{}'.format(path, 'key.pem'))


@pytest.mark.parametrize('f,path', [
    (check_call, 'subprocess32.check_call'),
    (check_output, 'subprocess32.check_output')
])
def test_check_call_output(f, path):
    with mock.patch(path) as mocked:
        f(['test', 'one', '--two'], False, 0, None, testing='yes')
    assert mocked.call_count == 1
    args, kwargs = mocked.call_args
    assert args[1:] == (False, 0, None)
    assert kwargs == {'testing': 'yes'}
    assert args[0][-3:] == ['test', 'one', '--two']


def test_retrieve_credentials(fake_machine_credentials, fake_machine_name):
    with contextmanagers.temp_dir() as temp:
        retrieve_credentials(fake_machine_name, temp)
        assert os.path.exists(os.path.join(temp, 'ca.pem'))
        assert os.path.exists(os.path.join(temp, 'cert.pem'))
        assert os.path.exists(os.path.join(temp, 'key.pem'))

        with pytest.raises(MachineNotFoundError):
            retrieve_credentials('nonexistent', temp)


def test_get_url(fake_machine_credentials, fake_machine_name):
    with mock.patch('deploy.docker_machine.check_output') as mocked:
        mocked.return_value = 'export DOCKER_HOST=tcp://test'
        url = get_url(fake_machine_name)
    assert url == 'tcp://test'
    mocked.assert_called_once_with(['env', fake_machine_name])

    with pytest.raises(MachineNotFoundError):
        get_url('nonexistent')
