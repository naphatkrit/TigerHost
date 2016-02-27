from tigerhost.api_client import ApiClientResponseError
from tigerhost.entry import entry
from tigerhost.vcs.git import GitVcs


def test_list_apps_success(runner, saved_user, fake_api_client):
    """
    @type runner: click.testing.CliRunner
    @type fake_api_client: mock.Mock
    """
    fake_api_client.get_all_applications.return_value = ['app1', 'app2']
    result = runner.invoke(entry, ['apps'])
    assert result.exit_code == 0
    assert 'app1' in result.output
    assert 'app2' in result.output


def test_create_app(runner, saved_user, fake_api_client):
    app = 'app1'
    result = runner.invoke(entry, ['create', app])
    assert result.exit_code == 0
    assert app in result.output
    fake_api_client.create_application.assert_called_once_with(app)


def test_create_app_in_repo(runner, make_git_repo, saved_user, fake_api_client):
    app = 'app1'
    fake_api_client.get_application_git_remote.return_value = 'remote'
    result = runner.invoke(entry, ['create', app])
    assert result.exit_code == 0
    assert app in result.output
    fake_api_client.create_application.assert_called_once_with(app)
    git = GitVcs()
    assert git.get_remotes()['tigerhost'] == 'remote'


def test_create_app_in_repo_failed_connection(runner, make_git_repo, saved_user, fake_api_client):
    app = 'app1'
    fake_api_client.get_application_git_remote.side_effect = ApiClientResponseError(None)
    result = runner.invoke(entry, ['create', app])
    assert result.exit_code == 0
    assert app in result.output
    fake_api_client.create_application.assert_called_once_with(app)
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
    fake_api_client.create_application.assert_called_once_with(app)
    assert git.get_remotes()['tigerhost'] == 'remote'


def test_create_app_in_repo_old_n(runner, make_git_repo, saved_user, fake_api_client):
    app = 'app1'
    git = GitVcs()
    git.add_remote('tigerhost', 'old')
    fake_api_client.get_application_git_remote.return_value = 'remote'
    result = runner.invoke(entry, ['create', app], input='n')
    assert result.exit_code == 0
    assert app in result.output
    fake_api_client.create_application.assert_called_once_with(app)
    assert git.get_remotes()['tigerhost'] == 'old'


def test_destroy_app(runner, saved_user, fake_api_client):
    app = 'app1'
    result = runner.invoke(entry, ['apps:destroy', '--app', app])
    assert result.exit_code == 0
    assert app in result.output
    fake_api_client.delete_application.assert_called_once_with(app)
