from tigerhost.entry import entry
from tigerhost.commands.logs import _available_colors


def test_get_logs(runner, saved_user, fake_api_client):
    """
    @type runner: click.testing.CliRunner
    @type fake_api_client: mock.Mock
    """
    logs = []
    for i in range(2 * len(_available_colors)):
        logs.append({
            'process': '{}'.format(i),
            'message': 'this is a test message{}'.format(i),
            'timestamp': 'time stamp{}'.format(i),
            'app': 'app{}'.format(i),
        })
    fake_api_client.get_application_logs.return_value = logs
    result = runner.invoke(entry, ['logs', '--app', 'app'])
    assert result.exit_code == 0
    for log in logs:
        assert log['process'] in result.output
        assert log['message'] in result.output
        assert log['timestamp'] in result.output
        assert log['app'] in result.output
    fake_api_client.get_application_logs.assert_called_once_with('app', lines=None)


def test_get_logs_num(runner, saved_user, fake_api_client):
    """
    @type runner: click.testing.CliRunner
    @type fake_api_client: mock.Mock
    """
    logs = []
    for i in range(2 * len(_available_colors)):
        logs.append({
            'process': '{}'.format(i),
            'message': 'this is a test message{}'.format(i),
            'timestamp': 'time stamp{}'.format(i),
            'app': 'app{}'.format(i),
        })
    fake_api_client.get_application_logs.return_value = logs
    result = runner.invoke(entry, ['logs', '--app', 'app', '--num', '10'])
    assert result.exit_code == 0
    for log in logs:
        assert log['process'] in result.output
        assert log['message'] in result.output
        assert log['timestamp'] in result.output
        assert log['app'] in result.output
    fake_api_client.get_application_logs.assert_called_once_with('app', lines=10)
