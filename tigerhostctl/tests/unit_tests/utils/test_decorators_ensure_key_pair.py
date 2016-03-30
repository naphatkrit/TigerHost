import botocore
import click
import mock
import os
import pytest

from tigerhost import exit_codes
from tigerhost.utils import contextmanagers

from tigerhostctl.utils.decorators import ensure_key_pair


@pytest.fixture(scope='function')
def fake_key_pair_info():
    mocked = mock.Mock()
    mocked.delete = mock.Mock()
    type(mocked).key_fingerprint = mock.PropertyMock()
    return mocked


@pytest.fixture(scope='function')
def fake_ec2_resource(fake_key_pair_info):
    mocked_key_pair_init = mock.Mock()
    mocked_key_pair_init.return_value = fake_key_pair_info
    mocked = mock.Mock()
    mocked.KeyPair = mocked_key_pair_init
    return mocked


@pytest.fixture(scope='function')
def fake_ec2_client():
    mocked = mock.Mock()
    mocked.import_key_pair = mock.Mock()
    mocked.create_key_pair = mock.Mock()
    return mocked


@click.command()
@ensure_key_pair('test')
def dummy():
    pass


@pytest.yield_fixture(scope='function')
def fake_ssh_folder():
    with contextmanagers.temp_dir() as temp:
        yield temp


@pytest.fixture(scope='function')
def fake_ssh_path_function(fake_ssh_folder):
    def fake(name):
        return os.path.join(fake_ssh_folder, name)
    return fake


class FakeClientError(botocore.exceptions.ClientError):

    def __init__(self):
        pass


def test_ensure_key_pair_nonexist_local(runner, fake_ec2_resource, fake_ec2_client, fake_ssh_path_function, fake_key_pair_info):
    fake_ec2_client.create_key_pair.return_value = {
        'KeyMaterial': 'test key'
    }
    with mock.patch('boto3.resource') as mocked_resource, mock.patch('boto3.client') as mocked_client, mock.patch('tigerhostctl.utils.decorators._ssh_path', new=fake_ssh_path_function):
        mocked_resource.return_value = fake_ec2_resource
        mocked_client.return_value = fake_ec2_client
        result = runner.invoke(dummy, input='\n')
    assert result.exit_code == exit_codes.SUCCESS
    fake_ec2_resource.KeyPair.assert_called_once_with('test')
    fake_key_pair_info.delete.assert_called_once_with()
    fake_ec2_client.create_key_pair.assert_called_once_with(KeyName='test')
    with open(fake_ssh_path_function('test'), 'r') as f:
        assert f.read() == 'test key'


def test_ensure_key_pair_nonexist_local_private(runner, fake_ec2_resource, fake_ec2_client, fake_ssh_path_function, fake_key_pair_info):
    fake_ec2_client.create_key_pair.return_value = {
        'KeyMaterial': 'test key'
    }
    type(fake_key_pair_info).key_fingerprint = mock.PropertyMock(side_effect=FakeClientError)
    assert not os.system('touch {}'.format(fake_ssh_path_function('test')))
    with mock.patch('boto3.resource') as mocked_resource, mock.patch('boto3.client') as mocked_client, mock.patch('tigerhostctl.utils.decorators._ssh_path', new=fake_ssh_path_function):
        mocked_resource.return_value = fake_ec2_resource
        mocked_client.return_value = fake_ec2_client
        result = runner.invoke(dummy, input='\n')
    assert result.exit_code == exit_codes.SUCCESS
    fake_ec2_resource.KeyPair.assert_called_once_with('test')
    fake_key_pair_info.delete.assert_called_once_with()
    fake_ec2_client.create_key_pair.assert_called_once_with(KeyName='test')
    with open(fake_ssh_path_function('test'), 'r') as f:
        assert f.read() == 'test key'


def test_ensure_key_pair_nonexist_local_public(runner, fake_ec2_resource, fake_ec2_client, fake_ssh_path_function, fake_key_pair_info):
    fake_ec2_client.create_key_pair.return_value = {
        'KeyMaterial': 'test key'
    }
    assert not os.system('touch {}.pub'.format(fake_ssh_path_function('test')))
    with mock.patch('boto3.resource') as mocked_resource, mock.patch('boto3.client') as mocked_client, mock.patch('tigerhostctl.utils.decorators._ssh_path', new=fake_ssh_path_function):
        mocked_resource.return_value = fake_ec2_resource
        mocked_client.return_value = fake_ec2_client
        result = runner.invoke(dummy, input='\n')
    assert result.exit_code == exit_codes.SUCCESS
    fake_ec2_resource.KeyPair.assert_called_once_with('test')
    fake_key_pair_info.delete.assert_called_once_with()
    fake_ec2_client.create_key_pair.assert_called_once_with(KeyName='test')
    with open(fake_ssh_path_function('test'), 'r') as f:
        assert f.read() == 'test key'


def test_ensure_key_pair_exist_local(runner, fake_ec2_resource, fake_ec2_client, fake_ssh_path_function, fake_key_pair_info):
    type(fake_key_pair_info).key_fingerprint = mock.PropertyMock(
        side_effect=FakeClientError)
    assert not os.system('touch {}'.format(fake_ssh_path_function('test')))
    with open(fake_ssh_path_function('test') + '.pub', 'w') as f:
        f.write('test key')
    with mock.patch('boto3.resource') as mocked_resource, mock.patch('boto3.client') as mocked_client, mock.patch('tigerhostctl.utils.decorators._ssh_path', new=fake_ssh_path_function):
        mocked_resource.return_value = fake_ec2_resource
        mocked_client.return_value = fake_ec2_client
        result = runner.invoke(dummy, input='\n')
    assert result.exit_code == exit_codes.SUCCESS
    fake_ec2_resource.KeyPair.assert_called_once_with('test')
    fake_ec2_client.import_key_pair.assert_called_once_with(
        KeyName='test', PublicKeyMaterial='test key')


def test_ensure_key_pair_exist_normal(runner, fake_ec2_resource, fake_ssh_path_function, fake_key_pair_info):
    assert not os.system('touch {}'.format(fake_ssh_path_function('test')))
    with mock.patch('boto3.resource') as mocked_resource, mock.patch('tigerhostctl.utils.decorators._ssh_path', new=fake_ssh_path_function):
        mocked_resource.return_value = fake_ec2_resource
        result = runner.invoke(dummy, input='\n')
    assert result.exit_code == exit_codes.SUCCESS
    fake_ec2_resource.KeyPair.assert_called_once_with('test')
