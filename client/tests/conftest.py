import mock
import os
import pytest
import random
import string

from click.testing import CliRunner

from tigerhost.private_dir import ensure_private_dir_exists
from tigerhost.utils.contextmanagers import temp_dir, temp_file


@pytest.yield_fixture(scope='function')
def runner():
    runner = CliRunner()
    with runner.isolated_filesystem():
        yield runner


@pytest.fixture(scope='function')
def make_git_repo(runner):
    assert not os.system('git init')


@pytest.yield_fixture(scope='function', autouse=True)
def fake_private_dir():
    with temp_dir() as path:
        new_private_dir = os.path.join(path, '.tigerhost')
        with mock.patch('tigerhost.private_dir._private_dir_path', new=new_private_dir):
            yield


@pytest.fixture(scope='function')
def ensure_private_dir(fake_private_dir):
    ensure_private_dir_exists()


@pytest.fixture(scope='function')
def public_key():
    # taken randomly from the internet
    return """ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAyyA8wePstPC69PeuHFtOwyTecByonsHFAjHbVnZ+h0dpomvLZxUtbknNj3+c7MPYKqKBOx9gUKV/diR/mIDqsb405MlrI1kmNR9zbFGYAAwIH/Gxt0Lv5ffwaqsz7cECHBbMojQGEz3IH3twEvDfF6cu5p00QfP0MSmEi/eB+W+h30NGdqLJCziLDlp409jAfXbQm/4Yx7apLvEmkaYSrb5f/pfvYv1FEV1tS8/J7DgdHUAWo6gyGUUSZJgsyHcuJT7v9Tf0xwiFWOWL9WsWXa9fCKqTeYnYJhHlqfinZRnT/+jkz0OZ7YmXo6j4Hyms3RCOqenIX1W6gnIn+eQIkw== This is the key's comment{}
""".format(''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(12)))


@pytest.yield_fixture(scope='function')
def public_key_path(public_key):
    with temp_file() as path:
        with open(path, 'w') as f:
            f.write(public_key)
        yield path
