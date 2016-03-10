from tigerhost.entry import entry


def test_list_addons(runner, saved_user, fake_api_client):
    """
    @type runner: click.testing.CliRunner
    @type fake_api_client: mock.Mock
    """
    addons = [{
        'addon': 'postgres',
        'name': 'fun-monkey-12d',
    }, {
        'addon': 'secret',
        'name': 'sad-bunny-1234',
    }]
    fake_api_client.get_application_addons.return_value = addons
    result = runner.invoke(entry, ['addons', '--app', 'app'])
    assert result.exit_code == 0
    for x in addons:
        assert x['name'] in result.output
        assert x['addon'] in result.output
    fake_api_client.get_application_addons.assert_called_once_with('app')


def test_create_addons(runner, saved_user, fake_api_client):
    """
    @type runner: click.testing.CliRunner
    @type fake_api_client: mock.Mock
    """
    fake_api_client.create_application_addon.return_value = {
        'message': 'test message', 'name': 'fun-monkey-12d'}
    result = runner.invoke(
        entry, ['addons:create', '--app', 'app', 'postgres'])
    assert result.exit_code == 0
    assert 'test message' in result.output
    assert 'fun-monkey-12d' in result.output
    fake_api_client.create_application_addon.assert_called_once_with(
        'app', 'postgres')


def test_delete_addons(runner, saved_user, fake_api_client):
    """
    @type runner: click.testing.CliRunner
    @type fake_api_client: mock.Mock
    """
    fake_api_client.delete_application_addon.return_value = {
        'message': 'test message'}
    result = runner.invoke(
        entry, ['addons:destroy', '--app', 'app', 'fun-monkey-12d'])
    assert result.exit_code == 0
    assert 'test message' in result.output
    fake_api_client.delete_application_addon.assert_called_once_with(
        'app', 'fun-monkey-12d')
