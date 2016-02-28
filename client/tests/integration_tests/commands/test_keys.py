import pytest

from tigerhost.entry import entry


@pytest.mark.parametrize('key_name', ['keyname', 'key_name', 'key-name', 'KeyName'])
def test_keys(runner, logged_in_user, public_key_path, key_name):
    """
    @type runner: click.testing.CliRunner
    """
    result = runner.invoke(entry, ['keys:add', key_name, public_key_path])
    assert result.exit_code == 0
    result = runner.invoke(entry, ['keys'])
    assert result.exit_code == 0
    assert key_name in result.output
    result = runner.invoke(entry, ['keys:remove', key_name])
    assert result.exit_code == 0
    result = runner.invoke(entry, ['keys'])
    assert key_name not in result.output
