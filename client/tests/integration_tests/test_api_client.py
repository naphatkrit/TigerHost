import pytest

from tigerhost.api_client import ApiClientAuthenticationError, ApiClientResponseError


def test_authentication_failure(api_client):
    api_client.api_key = '123'
    with pytest.raises(ApiClientAuthenticationError):
        api_client.get_all_applications()


@pytest.yield_fixture
def create_application(api_client, app_id):
    """
    @type api_client: tigerhost.api_client.ApiClient
    """
    api_client.create_application(app_id)
    try:
        yield
    finally:
        api_client.delete_application(app_id)


def test_application_creation(api_client, app_id):
    """
    @type api_client: tigerhost.api_client.ApiClient
    """
    # create application
    api_client.create_application(app_id)

    with pytest.raises(ApiClientResponseError):
        api_client.create_application(app_id)

    found = False
    for backend, ids in api_client.get_all_applications().iteritems():
        if app_id in ids:
            found = True
            break
    assert found

    # delete application
    api_client.delete_application(app_id)

    found = False
    for backend, ids in api_client.get_all_applications().iteritems():
        if app_id in ids:
            found = True
            break
    assert not found

    with pytest.raises(ApiClientResponseError):
        api_client.delete_application(app_id)


def test_application_creation_with_backend(api_client, app_id):
    """
    @type api_client: tigerhost.api_client.ApiClient
    """
    # pick a backend
    backend = api_client.get_backends()['backends'][0]

    # create application
    api_client.create_application(app_id, backend)

    with pytest.raises(ApiClientResponseError):
        api_client.create_application(app_id)

    assert api_client.get_all_applications()[backend] == [app_id]

    # delete application
    api_client.delete_application(app_id)

    assert api_client.get_all_applications()[backend] == []

    with pytest.raises(ApiClientResponseError):
        api_client.delete_application(app_id)


def test_application_env_variables(api_client, app_id, create_application):
    """
    @type api_client: tigerhost.api_client.ApiClient
    """
    # test environmental variables
    bindings = {
        'TESTING1': '1',
        'TESTING2': '2'
    }
    old_vars = api_client.get_application_env_variables(app_id)
    api_client.set_application_env_variables(
        app_id, bindings)

    old_vars_updated = old_vars.copy()
    old_vars_updated.update(bindings)

    new_vars = api_client.get_application_env_variables(app_id)
    assert new_vars == old_vars_updated

    api_client.set_application_env_variables(
        app_id, {key: None for key in bindings})
    new_vars_deleted = api_client.get_application_env_variables(
        app_id)
    assert old_vars == new_vars_deleted

    # test deletion and creation at the same time
    api_client.set_application_env_variables(app_id, {"TESTING1": '1'})
    api_client.set_application_env_variables(
        app_id, {"TESTING1": None, "TESTING2": "2"})
    assert api_client.get_application_env_variables(app_id) == {
        'TESTING2': '2'
    }


def test_application_git_remote(api_client, app_id, create_application):
    remote = api_client.get_application_git_remote(app_id)
    assert 'ssh' in remote
    assert 'git@' in remote
    assert '.git' in remote


def test_application_domains(api_client, app_id, create_application):
    domain = '{}.example.com'.format(app_id)
    old_domains = api_client.get_application_domains(app_id)
    api_client.add_application_domain(app_id, domain)
    assert api_client.get_application_domains(
        app_id) == old_domains + [domain]

    # can't add a domain twice
    with pytest.raises(ApiClientResponseError):
        api_client.add_application_domain(app_id, domain)

    api_client.remove_application_domain(app_id, domain)
    assert api_client.get_application_domains(
        app_id) == old_domains

    # can't remove a non-existent domain
    with pytest.raises(ApiClientResponseError):
        api_client.remove_application_domain(app_id, domain)


def test_run_command(api_client, app_id, create_application):
    with pytest.raises(ApiClientResponseError):
        api_client.run_command(app_id, 'echo 1 2 3')


def test_application_ownership(api_client, app_id, create_application, api_client2, username, username2):
    """
    @type api_client: tigerhost.api_client.ApiClient
    @type api_client2: tigerhost.api_client.ApiClient
    """
    assert api_client.get_application_owner(app_id) == username

    api_client.set_application_owner(app_id, username2)
    with pytest.raises(ApiClientResponseError):
        api_client.get_application_owner(
            app_id)  # no permissions

    api_client2.get_application_owner(app_id) == username2

    # set the ownership back so the fixture can delete the application
    api_client2.set_application_owner(app_id, username)


def test_application_collaborators(api_client, app_id, create_application, api_client2, username, username2):
    """
    @type api_client: tigerhost.api_client.ApiClient
    @type api_client2: tigerhost.api_client.ApiClient
    """
    assert api_client.get_application_collaborators(app_id) == [
    ]

    # add collaborator
    api_client.add_application_collaborator(app_id, username2)
    assert api_client.get_application_collaborators(app_id) == [
        username2]

    # check if collaborator actually has some permissions
    api_client2.get_application_owner(app_id) == username
    # ...but not all permissions
    with pytest.raises(ApiClientResponseError):
        api_client2.set_application_owner(app_id, username2)

    # remove collaborator
    api_client.remove_application_collaborator(
        app_id, username2)
    assert api_client.get_application_collaborators(app_id) == [
    ]
    with pytest.raises(ApiClientResponseError):
        api_client.remove_application_collaborator(
            app_id, username2)

    # no longer has any permissions
    with pytest.raises(ApiClientResponseError):
        api_client2.get_application_owner(app_id)


def test_application_addons(api_client, app_id, create_application):
    """
    @type api_client: tigerhost.api_client.ApiClient
    """
    result = api_client.create_application_addon(app_id, 'secret')
    assert 'message' in result

    name = result['display_name']
    addons = api_client.get_application_addons(app_id)
    assert len(addons) == 1
    assert addons[0]['display_name'] == name
    assert addons[0]['provider_name'] == 'secret'

    addon = api_client.get_application_addon(app_id, name)
    assert addons[0] == addon

    result = api_client.delete_application_addon(app_id, name)

    addons = api_client.get_application_addons(app_id)
    assert len(addons) == 0


def test_keys(api_client, public_key):
    """
    @type api_client: tigerhost.api_client.ApiClient
    """
    # pick a backend
    backend = api_client.get_backends()['default']

    key_name = 'key_name'
    old_keys = api_client.get_keys()

    api_client.add_key(key_name, public_key, backend)
    new_keys = api_client.get_keys()
    assert new_keys[backend] == old_keys[backend] + \
        [{'key_name': key_name, 'key': public_key}]

    with pytest.raises(ApiClientResponseError):
        api_client.add_key(key_name, public_key, backend)

    api_client.remove_key(key_name, backend)
    assert api_client.get_keys() == old_keys

    with pytest.raises(ApiClientResponseError):
        api_client.remove_key(key_name, backend)
