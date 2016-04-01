import os
import pytest
import yaml

from tigerhost.utils import contextmanagers

from deploy.commands.addons.create import _generate_compose_file


_compose_file_content = '''
version: '2'
services:
    docs:
        build: ./docs
'''


@pytest.yield_fixture
def project_path():
    with contextmanagers.temp_dir() as temp:
        os.mkdir(os.path.join(temp, 'proxy'))
        with open(os.path.join(temp, 'proxy/docker-compose.prod.template.yml'), 'w') as f:
            f.write(_compose_file_content)
        yield temp


def test_compose_file_no_database(project_path):
    _generate_compose_file(project_path, None)
    with open(os.path.join(project_path, 'proxy/docker-compose.prod.yml'), 'r') as f:
        data = yaml.safe_load(f)
    assert len(data['services'].keys()) == 1


def test_compose_file_with_database(project_path):
    _generate_compose_file(project_path, 'container_name')
    with open(os.path.join(project_path, 'proxy/docker-compose.prod.yml'), 'r') as f:
        data = yaml.safe_load(f)
    assert len(data['services'].keys()) == 2
    assert 'container_name' in data['services']
