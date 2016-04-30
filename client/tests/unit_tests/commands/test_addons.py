from tigerhost.entry import entry


def test_list_addons(runner, saved_user, fake_api_client):
    """
    @type runner: click.testing.CliRunner
    @type fake_api_client: mock.Mock
    """
    addons = [{
        'provider_name': 'postgres',
        'display_name': 'fun-monkey-12d',
        'state': 'ready',
    }, {
        'provider_name': 'secret',
        'display_name': 'sad-bunny-1234',
        'state': 'waiting_for_provision',
    }]
    fake_api_client.get_application_addons.return_value = addons
    result = runner.invoke(entry, ['addons', '--app', 'app'])
    assert result.exit_code == 0
    for x in addons:
        assert x['display_name'] in result.output
        assert x['provider_name'] in result.output
        assert x['state'] in result.output
    fake_api_client.get_application_addons.assert_called_once_with('app')


def test_create_addons(runner, saved_user, fake_api_client):
    """
    @type runner: click.testing.CliRunner
    @type fake_api_client: mock.Mock
    """
    fake_api_client.create_application_addon.return_value = {
        'message': 'test message', 'addon': {'display_name': 'fun-monkey-12d'}}
    result = runner.invoke(
        entry, ['addons:create', '--app', 'app', 'postgres'])
    assert result.exit_code == 0
    assert 'test message' in result.output
    assert 'fun-monkey-12d' in result.output
    fake_api_client.create_application_addon.assert_called_once_with(
        'app', 'postgres', config_customization=None)


def test_create_addons_with_config_customization(runner, saved_user, fake_api_client):
    """
    @type runner: click.testing.CliRunner
    @type fake_api_client: mock.Mock
    """
    fake_api_client.create_application_addon.return_value = {
        'message': 'test message', 'addon': {'display_name': 'fun-monkey-12d'}}
    result = runner.invoke(
        entry, ['addons:create', '--app', 'app', 'postgres', '--attach-as', 'TEST'])
    assert result.exit_code == 0
    assert 'test message' in result.output
    assert 'fun-monkey-12d' in result.output
    fake_api_client.create_application_addon.assert_called_once_with(
        'app', 'postgres', config_customization='TEST')


def test_wait_addons(runner, saved_user, fake_api_client):
    """
    @type runner: click.testing.CliRunner
    @type fake_api_client: mock.Mock
    """
    fake_api_client.get_application_addon.side_effect = [
        {
            'state': 'waiting_for_provision',
        },
        {
            'state': 'waiting_for_provision',
        },
        {
            'state': 'waiting_for_provision',
        },
        {
            'state': 'provisioned',
        },
        {
            'state': 'ready',
        },
    ]
    result = runner.invoke(
        entry, ['addons:wait', 'fun-monkey-12d', '--app', 'app', '--interval', '0'])
    assert result.exit_code == 0
    assert fake_api_client.get_application_addon.call_count == 5
    assert 'waiting_for_provision' in result.output
    assert 'provisioned' in result.output
    assert 'ready' in result.output


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
