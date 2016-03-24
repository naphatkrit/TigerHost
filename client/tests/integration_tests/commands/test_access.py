from tigerhost.entry import entry


def test_access(runner, make_app, username, username2):
    """
    @type runner: click.testing.CliRunner
    """
    result = runner.invoke(entry, ['access'])
    assert result.exit_code == 0
    assert username in result.output  # owner
    assert username2 not in result.output  # collaborator

    result = runner.invoke(entry, ['access:add', username2])
    assert result.exit_code == 0

    result = runner.invoke(entry, ['access'])
    assert result.exit_code == 0
    assert username in result.output  # owner
    assert username2 in result.output  # collaborator

    result = runner.invoke(entry, ['access:remove', username2])
    assert result.exit_code == 0

    result = runner.invoke(entry, ['access'])
    assert result.exit_code == 0
    assert username in result.output  # owner
    assert username2 not in result.output  # collaborator
