from tigerhost.entry import entry


def test_run_command(runner, saved_user, fake_api_client):
    """
    @type runner: click.testing.CliRunner
    @type fake_api_client: mock.Mock
    """
    command = 'echo 1 2 3'
    fake_api_client.run_command.return_value = {
        'exit_code': 0,
        'output': '1 2 3\n',
    }
    result = runner.invoke(entry, ['run', '--app', 'app'] + command.split(' '))
    assert result.exit_code == 0
    assert '1 2 3' in result.output
    fake_api_client.run_command.assert_called_once_with('app', command)

    fake_api_client.run_command.return_value = {
        'exit_code': 1,
        'output': '1 2 3\n',
    }
    result = runner.invoke(entry, ['run', '--app', 'app'] + command.split(' '))
    assert result.exit_code == 1
    assert '1 2 3' in result.output
