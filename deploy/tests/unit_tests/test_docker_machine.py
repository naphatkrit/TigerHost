import mock
import os
import pytest

from tigerhost.utils import contextmanagers

from deploy.docker_machine import check_call, check_output, retrieve_credentials


@pytest.yield_fixture
def fake_machine_storage_path():
    with contextmanagers.temp_dir() as temp:
        os.makedirs('{}/machines/test_machine'.format(temp))
        assert not os.system('touch {}/machines/test_machine/{}'.format(temp, 'ca.pem'))
        assert not os.system('touch {}/machines/test_machine/{}'.format(temp, 'cert.pem'))
        assert not os.system('touch {}/machines/test_machine/{}'.format(temp, 'key.pem'))
        yield temp


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


def test_retrieve_credentials(fake_machine_storage_path):
    with mock.patch('deploy.docker_machine.docker_machine_storage_path') as mocked, contextmanagers.temp_dir() as temp:
        mocked.return_value = fake_machine_storage_path
        retrieve_credentials('test_machine', temp)
        assert os.path.exists(os.path.join(temp, 'ca.pem'))
        assert os.path.exists(os.path.join(temp, 'cert.pem'))
        assert os.path.exists(os.path.join(temp, 'key.pem'))
