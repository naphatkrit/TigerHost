import click

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
