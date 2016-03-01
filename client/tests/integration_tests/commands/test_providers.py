from tigerhost.entry import entry


def test_providers(runner, logged_in_user):
    """
    @type runner: click.testing.CliRunner
    """
    result = runner.invoke(entry, ['providers'])
    assert result.exit_code == 0
