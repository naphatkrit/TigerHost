from tigerhost.entry import entry


def test_get_users(runner, saved_user, fake_api_client):
    """
    @type runner: click.testing.CliRunner
    @type fake_api_client: mock.Mock
    """
    owner = 'userA'
    collaborators = ['userB', 'userC']
    fake_api_client.get_application_owner.return_value = owner
    fake_api_client.get_application_collaborators.return_value = collaborators
    result = runner.invoke(entry, ['access', '--app', 'app'])
    assert result.exit_code == 0
    assert owner in result.output
    for x in collaborators:
        assert x in result.output
    fake_api_client.get_application_owner.assert_called_once_with('app')
    fake_api_client.get_application_collaborators.assert_called_once_with(
        'app')


def test_add_access(runner, saved_user, fake_api_client):
    """
    @type runner: click.testing.CliRunner
    @type fake_api_client: mock.Mock
    """
    user = 'userB'
    result = runner.invoke(entry, ['access:add', '--app', 'app', user])
    assert result.exit_code == 0
    assert user in result.output
    fake_api_client.add_application_collaborator.assert_called_once_with(
        'app', user)


def test_remove_access(runner, saved_user, fake_api_client):
    """
    @type runner: click.testing.CliRunner
    @type fake_api_client: mock.Mock
    """
    user = 'userB'
    result = runner.invoke(entry, ['access:remove', '--app', 'app', user])
    assert result.exit_code == 0
    assert user in result.output
    fake_api_client.remove_application_collaborator.assert_called_once_with(
        'app', user)
