from tigerhost.entry import entry


def test_config(runner, make_app):
    """
    @type runner: click.testing.CliRunner
    """
    bindings = {
        'TEST1': '123',
        'TEST2': '3lkjelk',
    }
    result = runner.invoke(entry, ['config:set'] +
                           ['{}={}'.format(k, v) for k, v in bindings.iteritems()])
    assert result.exit_code == 0

    result = runner.invoke(entry, ['config'])
    assert result.exit_code == 0
    for k, v in bindings.iteritems():
        assert '{}={}'.format(k, v) in result.output

    bindings.pop('TEST1')
    result = runner.invoke(entry, ['config:unset', 'TEST1'])
    assert result.exit_code == 0

    result = runner.invoke(entry, ['config'])
    assert result.exit_code == 0
    for k, v in bindings.iteritems():
        assert '{}={}'.format(k, v) in result.output
