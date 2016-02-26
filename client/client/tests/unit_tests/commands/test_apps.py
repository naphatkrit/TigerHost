from tigerhost.entry import entry


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
