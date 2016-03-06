from tigerhost.entry import entry


def test_app(runner, logged_in_user, app_id):
    """
    @type runner: click.testing.CliRunner
    """
    result = runner.invoke(entry, ['create', app_id])
    assert result.exit_code == 0
    assert app_id in result.output

    result = runner.invoke(entry, ['apps'])
    assert result.exit_code == 0
    assert app_id in result.output

    result = runner.invoke(entry, ['apps:destroy', '--app', app_id])
    assert result.exit_code == 0
    assert app_id in result.output

    result = runner.invoke(entry, ['apps'])
    assert result.exit_code == 0
    assert app_id not in result.output


def test_app_with_backend(runner, logged_in_user, app_id, backend):
    """
    @type runner: click.testing.CliRunner
    """
    result = runner.invoke(entry, ['create', app_id, '--backend', backend])
    assert result.exit_code == 0
    assert app_id in result.output

    result = runner.invoke(entry, ['apps'])
    assert result.exit_code == 0
    assert app_id in result.output

    result = runner.invoke(entry, ['apps:destroy', '--app', app_id])
    assert result.exit_code == 0
    assert app_id in result.output

    result = runner.invoke(entry, ['apps'])
    assert result.exit_code == 0
    assert app_id not in result.output
