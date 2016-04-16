import responses
import pytest
import urlparse

from api_server.clients.deis_authenticated_client import DeisAuthenticatedClient


@pytest.fixture
def deis_authenticated_client(fake_deis_url, token):
    return DeisAuthenticatedClient(fake_deis_url, token)


@responses.activate
def test_get_all_applications_success(deis_authenticated_client, fake_deis_url):
    """
    @type deis_authenticated_client: DeisAuthenticatedClient
    @type fake_deis_url: str
    """
    test_ids = ['testid1', 'testid2']
    responses.add(responses.GET, urlparse.urljoin(
        fake_deis_url, 'v1/apps'), status=200, json={
        "results": [{'id': x} for x in test_ids]}
    )
    ids = deis_authenticated_client.get_all_applications()
    assert set(ids) == set(test_ids)


@responses.activate
def test_create_application_success(deis_authenticated_client, fake_deis_url):
    """
    @type deis_authenticated_client: DeisAuthenticatedClient
    @type fake_deis_url: str
    """
    responses.add(responses.POST, urlparse.urljoin(
        fake_deis_url, 'v1/apps/'), status=201)
    deis_authenticated_client.create_application('testid')


@responses.activate
def test_delete_application_success(deis_authenticated_client, fake_deis_url):
    responses.add(responses.DELETE, urlparse.urljoin(
        fake_deis_url, 'v1/apps/{}/'.format('testid')), status=204)
    deis_authenticated_client.delete_application('testid')


@responses.activate
def test_set_application_env_variables_success(deis_authenticated_client, fake_deis_url):
    responses.add(responses.POST, urlparse.urljoin(
        fake_deis_url, 'v1/apps/{}/config/'.format('testid')), status=201)
    deis_authenticated_client.set_application_env_variables(
        'testid', {'TESTING': 'testing'})


@responses.activate
def test_get_application_env_variables_success(deis_authenticated_client, fake_deis_url):
    bindings = {'TESTING': 'testing'}
    responses.add(responses.GET, urlparse.urljoin(
        fake_deis_url, 'v1/apps/{}/config/'.format('testid')), status=200, json={'values': bindings})
    ret = deis_authenticated_client.get_application_env_variables('testid')
    assert ret == bindings


@responses.activate
def test_get_application_domains(deis_authenticated_client, fake_deis_url):
    domains = ['a.com', 'b.com']
    responses.add(responses.GET, urlparse.urljoin(
        fake_deis_url, 'v1/apps/{}/domains/'.format('testid')), status=200, json={'results': [{'domain': x} for x in domains]})
    ret = deis_authenticated_client.get_application_domains('testid')
    assert ret == domains


@responses.activate
def test_add_application_domain(deis_authenticated_client, fake_deis_url):
    domain = 'a.example.com'
    responses.add(responses.POST, urlparse.urljoin(
        fake_deis_url, 'v1/apps/{}/domains/'.format('testid')), status=201)
    deis_authenticated_client.add_application_domain('testid', domain)


@responses.activate
def test_remove_application_domain(deis_authenticated_client, fake_deis_url):
    domain = 'a.example.com'
    responses.add(responses.DELETE, urlparse.urljoin(
        fake_deis_url, 'v1/apps/{}/domains/{}'.format('testid', domain)), status=204)
    deis_authenticated_client.remove_application_domain('testid', domain)


@responses.activate
def test_run_command(deis_authenticated_client, fake_deis_url):
    command = 'echo 1 2 3'
    responses.add(responses.POST, urlparse.urljoin(
        fake_deis_url, 'v1/apps/{}/run/'.format('testid')), status=204, json=[0, '1 2 3\n'])
    result = deis_authenticated_client.run_command('testid', command)
    assert result['exit_code'] == 0
    assert result['output'] == '1 2 3\n'


@responses.activate
def test_get_application_owner(deis_authenticated_client, fake_deis_url):
    responses.add(responses.GET, urlparse.urljoin(
        fake_deis_url, 'v1/apps/{}/'.format('testid')), status=200, json={'owner': 'username'})
    assert deis_authenticated_client.get_application_owner(
        'testid') == 'username'


@responses.activate
def test_set_application_owner(deis_authenticated_client, fake_deis_url):
    responses.add(responses.POST, urlparse.urljoin(
        fake_deis_url, 'v1/apps/{}/'.format('testid')), status=200)
    deis_authenticated_client.set_application_owner('testid', 'username')


@responses.activate
def test_get_application_collaborators(deis_authenticated_client, fake_deis_url):
    users = ['user1', 'user2']
    responses.add(responses.GET, urlparse.urljoin(
        fake_deis_url, 'v1/apps/{}/perms/'.format('testid')), status=200, json={'users': users})
    ret = deis_authenticated_client.get_application_collaborators('testid')
    assert set(ret) == set(users)


@responses.activate
def test_add_application_collaborator(deis_authenticated_client, fake_deis_url):
    username = 'username'
    responses.add(responses.POST, urlparse.urljoin(
        fake_deis_url, 'v1/apps/{}/perms/'.format('testid')), status=201)
    deis_authenticated_client.add_application_collaborator('testid', username)


@responses.activate
def test_remove_application_collaborator(deis_authenticated_client, fake_deis_url):
    username = 'username'
    responses.add(responses.DELETE, urlparse.urljoin(
        fake_deis_url, 'v1/apps/{}/perms/{}'.format('testid', username)), status=204)
    deis_authenticated_client.remove_application_collaborator(
        'testid', username)


@responses.activate
def test_get_application_logs(deis_authenticated_client, fake_deis_url):
    responses.add(responses.GET, urlparse.urljoin(
        fake_deis_url, 'v1/apps/{}/logs/'.format('testid')), status=200, json='''2016-04-16T14:26:03UTC sample-python[run.1]: int(None)
2016-04-16T14:26:04UTC sample-python[run.2]:     some message
''')
    logs = deis_authenticated_client.get_application_logs(
        'testid')
    assert logs == [{
        'process': 'run.1',
        'message': 'int(None)',
        'timestamp': '2016-04-16T14:26:03UTC',
        'app': 'sample-python',
    }, {
        'process': 'run.2',
        'message': '    some message',
        'timestamp': '2016-04-16T14:26:04UTC',
        'app': 'sample-python',
    },
    ]


@responses.activate
def test_get_application_keys(deis_authenticated_client, fake_deis_url):
    keys = ['key1', 'key2']
    responses.add(responses.GET, urlparse.urljoin(
        fake_deis_url, 'v1/keys/'), status=200, json={'results': [{'id': x, 'public': x} for x in keys]})
    ret = deis_authenticated_client.get_keys()
    assert ret == [{'key_name': x, 'key': x} for x in keys]


@responses.activate
def test_add_application_key(deis_authenticated_client, fake_deis_url):
    responses.add(responses.POST, urlparse.urljoin(
        fake_deis_url, 'v1/keys/'), status=201)
    deis_authenticated_client.add_key('key_name', 'key')


@responses.activate
def test_remove_application_key(deis_authenticated_client, fake_deis_url):
    key_name = 'key_name'
    responses.add(responses.DELETE, urlparse.urljoin(
        fake_deis_url, 'v1/keys/{}'.format(key_name)), status=204)
    deis_authenticated_client.remove_key(key_name)
