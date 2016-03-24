from tigerhost.entry import entry


def test_add_remote(runner, make_git_repo, saved_user, fake_api_client):
    """
    @type runner: click.testing.CliRunner
    @type fake_api_client: mock.Mock
    """
    remote_url = 'url'
    fake_api_client.get_application_git_remote.return_value = remote_url
    result = runner.invoke(entry, ['git:remote', '--app', 'app'])
    assert result.exit_code == 0
    assert remote_url in result.output
    fake_api_client.get_application_git_remote.assert_called_once_with('app')
