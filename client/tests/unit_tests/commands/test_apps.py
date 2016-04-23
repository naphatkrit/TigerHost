from tigerhost.api_client import ApiClientResponseError
from tigerhost.entry import entry
from tigerhost.vcs.git import GitVcs


def test_list_apps_success(runner, saved_user, fake_api_client):
    """
    @type runner: click.testing.CliRunner
    @type fake_api_client: mock.Mock
    """
    fake_api_client.get_all_applications.return_value = {
        'backend1': ['app1', 'app2']
    }
    result = runner.invoke(entry, ['apps'])
    assert result.exit_code == 0
    assert 'backend1' in result.output
    assert 'app1' in result.output
    assert 'app2' in result.output
    fake_api_client.get_all_applications.assert_called_once_with()


def test_create_app(runner, saved_user, fake_api_client):
    app = 'app1'
    result = runner.invoke(entry, ['create', app])
    assert result.exit_code == 0
    assert app in result.output
    fake_api_client.create_application.assert_called_once_with(app, None)


def test_create_app_with_backend(runner, saved_user, fake_api_client):
    app = 'app1'
    result = runner.invoke(entry, ['create', app, '--backend', 'backend'])
    assert result.exit_code == 0
    assert app in result.output
    fake_api_client.create_application.assert_called_once_with(app, 'backend')


def test_create_app_in_repo(runner, make_git_repo, saved_user, fake_api_client):
    app = 'app1'
    fake_api_client.get_application_git_remote.return_value = 'remote'
    result = runner.invoke(entry, ['create', app])
    assert result.exit_code == 0
    assert app in result.output
    fake_api_client.create_application.assert_called_once_with(app, None)
    git = GitVcs()
    assert git.get_remotes()['tigerhost'] == 'remote'


def test_create_app_in_repo_failed_connection(runner, make_git_repo, saved_user, fake_api_client):
    app = 'app1'
    fake_api_client.get_application_git_remote.side_effect = ApiClientResponseError(
        None)
    result = runner.invoke(entry, ['create', app])
    assert result.exit_code == 0
    assert app in result.output
    fake_api_client.create_application.assert_called_once_with(app, None)
    git = GitVcs()
    assert 'tigerhost' not in git.get_remotes()


def test_create_app_in_repo_old_y(runner, make_git_repo, saved_user, fake_api_client):
    app = 'app1'
    git = GitVcs()
    git.add_remote('tigerhost', 'old')
    fake_api_client.get_application_git_remote.return_value = 'remote'
    result = runner.invoke(entry, ['create', app], input='y')
    assert result.exit_code == 0
    assert app in result.output
    fake_api_client.create_application.assert_called_once_with(app, None)
    assert git.get_remotes()['tigerhost'] == 'remote'


def test_create_app_in_repo_old_n(runner, make_git_repo, saved_user, fake_api_client):
    app = 'app1'
    git = GitVcs()
    git.add_remote('tigerhost', 'old')
    fake_api_client.get_application_git_remote.return_value = 'remote'
    result = runner.invoke(entry, ['create', app], input='n')
    assert result.exit_code == 0
    assert app in result.output
    fake_api_client.create_application.assert_called_once_with(app, None)
    assert git.get_remotes()['tigerhost'] == 'old'


def test_destroy_app_no_addons(runner, saved_user, fake_api_client):
    app = 'app1'
    fake_api_client.get_application_addons.return_value = []
    result = runner.invoke(entry, ['apps:destroy', '--app', app])
    assert result.exit_code == 0
    assert app in result.output
    fake_api_client.delete_application.assert_called_once_with(app)


def test_destroy_app_with_addons(runner, saved_user, fake_api_client):
    app = 'app1'
    addons = ['addon1', 'addon2', 'addon3']

    fake_api_client.get_application_addons.return_value = [{
        'display_name': x,
        'provider_name': x + '_provider',
    } for x in addons]
    result = runner.invoke(entry, ['apps:destroy', '--app', app])
    assert result.exit_code == 0
    assert app in result.output
    fake_api_client.delete_application.assert_called_once_with(app)
    for x in addons:
        fake_api_client.delete_application_addon.assert_any_call(app, x)


def test_transfer_app(runner, saved_user, fake_api_client):
    """
    @type runner: click.testing.CliRunner
    @type fake_api_client: mock.Mock
    """
    user = 'username'
    result = runner.invoke(
        entry, ['apps:transfer', '--app', 'app', user], input='y')
    assert result.exit_code == 0
    fake_api_client.set_application_owner.assert_called_once_with('app', user)

    result = runner.invoke(
        entry, ['apps:transfer', '--app', 'app', user], input='n')
    assert result.exit_code == 0
    # did not call set_application_owner again
    assert fake_api_client.set_application_owner.call_count == 1
