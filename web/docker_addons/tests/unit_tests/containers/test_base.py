import pytest


@pytest.mark.django_db
def test_get_docker_hostname(container):
    assert container.get_docker_hostname() == '192.168.99.100'


@pytest.mark.django_db
def test_run_container(container, container_info, fake_docker_client):
    host_config = {
        'config1': 'value1'
    }
    container_id = '1234'
    fake_docker_client.create_host_config.return_value = host_config
    fake_docker_client.create_container.return_value = {
        'Id': container_id,
    }

    container.run_container()

    container_info.refresh_from_db()
    assert container_info.container_id == container_id

    fake_docker_client.pull.assert_called_once_with(container.get_image())
    assert fake_docker_client.create_host_config.call_count == 1
    assert fake_docker_client.create_container.call_count == 1
    fake_docker_client.start.assert_called_once_with(container_id)


@pytest.mark.django_db
def test_stop_container(container, container_info, fake_docker_client):
    container_info.container_id = '123'
    container.stop_container()
    fake_docker_client.stop.assert_called_once_with('123')
