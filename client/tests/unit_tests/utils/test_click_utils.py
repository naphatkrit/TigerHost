import click
import pytest

from tigerhost import exit_codes
from tigerhost.utils import click_utils


def test_echo_heading(runner):
    heading = 'test heading'

    @click.command()
    def dummy():
        click_utils.echo_heading(heading, marker='-')

    output = runner.invoke(dummy)
    assert output.exit_code == exit_codes.SUCCESS
    assert output.output == '---> ' + heading + '\n'


@pytest.mark.parametrize('app_name,bash_complete_name', [
    ('tigerhost', 'TIGERHOST'),
    ('tigerhost-deploy', 'TIGERHOST_DEPLOY'),
])
def test_bash_complete_name(app_name, bash_complete_name):
    assert click_utils._bash_complete_name(app_name) == bash_complete_name


def test_bash_complete_command(runner):
    result = runner.invoke(click_utils.bash_complete_command('test-app'))
    assert result.exit_code == exit_codes.SUCCESS
    assert '_TEST_APP_COMPLETE=source test-app' in result.output
