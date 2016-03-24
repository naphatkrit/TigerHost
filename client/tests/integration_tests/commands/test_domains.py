from tigerhost.entry import entry


def test_domains(runner, make_app, app_id):
    """
    @type runner: click.testing.CliRunner
    """
    domain = '{}.example.com'.format(app_id)
    result = runner.invoke(entry, ['domains:add', domain])
    assert result.exit_code == 0

    result = runner.invoke(entry, ['domains'])
    assert result.exit_code == 0
    assert domain in result.output

    result = runner.invoke(entry, ['domains:remove', domain])
    assert result.exit_code == 0
    assert domain in result.output

    result = runner.invoke(entry, ['domains:remove', domain])
    assert result.exit_code == 2
