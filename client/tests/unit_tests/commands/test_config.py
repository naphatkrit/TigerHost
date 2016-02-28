from tigerhost.entry import entry


def test_list_config(runner, saved_user, fake_api_client):
    """
    @type runner: click.testing.CliRunner
    @type fake_api_client: mock.Mock
    """
    bindings = {
        'TEST1': '123',
        'TEST2': '3lkjelk',
    }
    fake_api_client.get_application_env_variables.return_value = bindings
    result = runner.invoke(entry, ['config', '--app', 'app'])
    assert result.exit_code == 0
    for k, v in bindings.iteritems():
        assert '{}={}'.format(k, v) in result.output
    fake_api_client.get_application_env_variables.assert_called_once_with(
        'app')


def test_set_config(runner, saved_user, fake_api_client):
    """
    @type runner: click.testing.CliRunner
    @type fake_api_client: mock.Mock
    """
    bindings = {
        'TEST1': '123',
        'TEST2': '3lkjelk',
    }

    result = runner.invoke(entry, ['config:set', '--app', 'app', '--'] + [
                           '{}={}'.format(k, v) for k, v in bindings.iteritems()])
    assert result.exit_code == 0
    for k, v in bindings.iteritems():
        assert '{}={}'.format(k, v) in result.output
    fake_api_client.set_application_env_variables.assert_called_once_with(
        'app', bindings)


def test_set_config_format_failure(runner, saved_user, fake_api_client):
    """
    @type runner: click.testing.CliRunner
    @type fake_api_client: mock.Mock
    """
    result = runner.invoke(entry, ['config:set', '--app', 'app', 'VAR'])
    assert result.exit_code == 2


def test_unset_config(runner, saved_user, fake_api_client):
    """
    @type runner: click.testing.CliRunner
    @type fake_api_client: mock.Mock
    """
    bindings = {
        'TEST1': '123',
        'TEST2': '3lkjelk',
    }

    result = runner.invoke(entry, [
                           'config:unset', '--app', 'app', '--'] + [k for k, _ in bindings.iteritems()])
    assert result.exit_code == 0
    for k in bindings:
        assert k in result.output
    fake_api_client.set_application_env_variables.assert_called_once_with(
        'app', {k: None for k in bindings})
