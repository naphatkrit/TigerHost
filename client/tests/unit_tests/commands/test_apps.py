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


def test_create_app(runner, saved_user, fake_api_client):
    app = 'app1'
    result = runner.invoke(entry, ['create', app])
    assert result.exit_code == 0
    assert app in result.output
    fake_api_client.create_application.assert_called_once_with(app)


def test_destroy_app(runner, saved_user, fake_api_client):
    app = 'app1'
    result = runner.invoke(entry, ['apps:destroy', '--app', app])
    assert result.exit_code == 0
    assert app in result.output
    fake_api_client.delete_application.assert_called_once_with(app)
