import os
import pytest
import yaml

from tigerhost.utils import contextmanagers

from deploy.commands.main.create import _generate_compose_file


_compose_file_content = '''
version: '2'
services:
    rabbitmq:
        image: rabbitmq
    redis:
        image: redis
    nginx:
        restart: always
        build: ./nginx
        ports:
            - "80:80"
        links:
            - web:web
        volumes_from:
            - docs
    docs:
        build: ./docs
    web:
        restart: always
        build: ./web
        command: bin/web.sh
        environment:
            DEIS_URL: http://deis.tigerhostapp.com
            BROKER_URL: amqp://guest:guest@rabbitmq:5672//
            CELERY_RESULT_BACKEND: redis://redis:6379/
            AWS_DEFAULT_REGION: us-east-1
            DOCKER_CERT_PATH: /code/credentials
            DOCKER_NETWORK: proxy_default

            # TODO: fill out the actual values for these variables
            DOCKER_HOST: tcp://54.209.153.101:2376
            DATABASE_URL: postgres://user:password@rds_host:5432/db_name
            SECRET: abcdefghijklmnopqrstuvwxyz
        expose:
            - "8000"
        links:
            - redis:redis
            - rabbitmq:rabbitmq
    worker:
        build: ./web
        command: bin/worker.sh
        environment:
            DEIS_URL: http://deis.tigerhostapp.com
            BROKER_URL: amqp://guest:guest@rabbitmq:5672//
            CELERY_RESULT_BACKEND: redis://redis:6379/
            AWS_DEFAULT_REGION: us-east-1
            DOCKER_CERT_PATH: /code/credentials
            DOCKER_NETWORK: proxy_default

            # TODO: fill out the actual values for these variables
            DOCKER_HOST: tcp://54.209.153.101:2376
            DATABASE_URL: postgres://user:password@rds_host:5432/db_name
            SECRET: abcdefghijklmnopqrstuvwxyz
        links:
            - redis:redis
            - rabbitmq:rabbitmq
'''


@pytest.yield_fixture
def project_path():
    with contextmanagers.temp_dir() as temp:
        with open(os.path.join(temp, 'docker-compose.prod.template.yml'), 'w') as f:
            f.write(_compose_file_content)
        yield temp


def test_compose_file(project_path):
    _generate_compose_file(project_path, 'database', 'docker', 'secret')
    with open(os.path.join(project_path, 'docker-compose.prod.yml'), 'r') as f:
        data = yaml.safe_load(f)
    assert data['services']['web']['environment']['DOCKER_HOST'] == 'docker'
    assert data['services']['web']['environment']['DATABASE_URL'] == 'database'
    assert data['services']['web']['environment']['SECRET'] == 'secret'

    assert data['services']['worker']['environment']['DOCKER_HOST'] == 'docker'
    assert data['services']['worker']['environment']['DATABASE_URL'] == 'database'
    assert data['services']['worker']['environment']['SECRET'] == 'secret'
