import click
import pytest

from tigerhost import exit_codes
from tigerhost.utils.click_utils import full_command_name


@click.command()
@click.pass_context
def command1(ctx):
    click.echo(full_command_name(ctx), nl=False)


@click.group()
def group1():
    pass

group1.add_command(command1)


@click.group('outer-group1')
def outer_group1():
    pass


outer_group1.add_command(group1)


@pytest.mark.parametrize('command, args, full_name', [
    (command1, [], 'command1'),
    (group1, ['command1'], 'group1 command1'),
    (outer_group1, ['group1', 'command1'], 'outer-group1 group1 command1')
])
def test_simple(runner, command, args, full_name):
    result = runner.invoke(command, args)
    assert result.exit_code == exit_codes.SUCCESS
    assert result.output == full_name
