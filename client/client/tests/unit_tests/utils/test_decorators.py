import click
import pytest

from tigerhost.utils import decorators


@click.command()
@click.pass_context
@decorators.print_markers
def passing_command(ctx):
    click.echo('Passing command with context')


@click.command()
@click.pass_context
@decorators.print_markers
def failing_command(ctx):
    raise Exception


@click.command()
@click.pass_context
@decorators.print_markers
def passing_command_with_context(ctx):
    click.echo('Command with context')


@pytest.mark.parametrize('command,exit_code', [
    (passing_command, 0),
    (failing_command, -1),
    (passing_command_with_context, 0),
])
def test_simple(runner, command, exit_code):
    result = runner.invoke(command)
    assert result.exit_code == exit_code
    assert '= tigerhost ' + command.name + ' =' in result.output
    assert '= end of tigerhost ' + command.name + ' =' in result.output
