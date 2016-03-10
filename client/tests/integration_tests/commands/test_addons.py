from tigerhost.entry import entry


def test_addons(runner, make_app, app_id):
    """
    @type runner: click.testing.CliRunner
    """
    result = runner.invoke(entry, ['addons:create', 'secret'])
    assert result.exit_code == 0

    name = result.output.split('\n')[1].split(':')[1].strip()

    result = runner.invoke(entry, ['addons'])
    assert result.exit_code == 0
    assert name in result.output
    assert 'secret' in result.output

    result = runner.invoke(entry, ['addons:destroy', name])
    assert result.exit_code == 0

    result = runner.invoke(entry, ['addons'])
    assert result.exit_code == 0
    assert name not in result.output
    assert 'secret' not in result.output
