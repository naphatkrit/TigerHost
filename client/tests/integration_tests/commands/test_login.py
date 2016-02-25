from tigerhost.entry import entry


def test_login_success(runner, username, api_key):
    result = runner.invoke(entry, ['login', '-u', username, '-a', api_key])
    assert result.exit_code == 0


def test_login_failure_auth(runner, username, api_key):
    result = runner.invoke(
        entry, ['login', '-u', username, '-a', api_key + '0'])
    assert result.exit_code == 2
    assert 'Please try again' in result.output
