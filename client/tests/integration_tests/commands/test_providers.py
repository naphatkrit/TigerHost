from tigerhost.entry import entry


def test_backends(runner, logged_in_user):
    """
    @type runner: click.testing.CliRunner
    """
    result = runner.invoke(entry, ['backends'])
    assert result.exit_code == 0
