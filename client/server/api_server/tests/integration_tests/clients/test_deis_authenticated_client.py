import pytest

from api_server.clients.deis_client_errors import DeisClientResponseError


@pytest.fixture
def deis_authenticated_client(deis_client, username, password, email):
    deis_client.register(username, password, email)
    return deis_client.login(username, password)


def test_application(deis_authenticated_client, app_id):
    """
    @type deis_authenticated_client: api_server.clients.deis_authenticated_client.DeisAuthenticatedClient
    """
    # create application
    deis_authenticated_client.create_application(app_id)

    with pytest.raises(DeisClientResponseError):
        deis_authenticated_client.create_application(app_id)

    ids = deis_authenticated_client.get_all_applications()
    assert ids == [app_id]

    # test environmental variables
    old_vars = deis_authenticated_client.get_application_env_variables(app_id)
    deis_authenticated_client.set_application_env_variables(
        app_id, {'TESTING': 'testing'})
    old_vars['TESTING'] = 'testing'
    new_vars = deis_authenticated_client.get_application_env_variables(app_id)
    assert new_vars == old_vars

    # delete application
    deis_authenticated_client.delete_application(app_id)

    ids = deis_authenticated_client.get_all_applications()
    assert ids == []

    with pytest.raises(DeisClientResponseError):
        deis_authenticated_client.delete_application(app_id)
