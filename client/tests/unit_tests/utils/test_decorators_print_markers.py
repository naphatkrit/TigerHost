import click
import pytest

from tigerhost.utils import decorators


@click.command()
@decorators.print_markers
def passing_command():
    click.echo('Passing command without context')


@click.command()
@click.pass_context
@decorators.print_markers
def failing_command(ctx):
    raise Exception


@click.command()
@click.pass_context
@decorators.print_markers
@decorators.catch_exception(Exception)
def failing_handled_command(ctx):
    raise Exception


@click.command()
@click.pass_context
@decorators.print_markers
def syntax_error_command(ctx):
    aldfjadfafd  # noqa


@click.command()
@click.pass_context
@decorators.print_markers
def exited_command(ctx):
    ctx.exit(3)


@click.command()
@click.pass_context
@decorators.print_markers
def aborted_command(ctx):
    ctx.abort()


@click.command()
@click.pass_context
@decorators.print_markers
def custom_exit_command(ctx):
    e = click.ClickException('custom message')
    e.exit_code = 5
    raise e


@click.command()
@click.pass_context
@decorators.print_markers
def default_exit_command(ctx):
    raise click.ClickException('custom message')


@click.command()
@click.pass_context
@decorators.print_markers
def passing_command_with_context(ctx):
    click.echo('Command with context')


@pytest.mark.parametrize('command,exit_code,end_template', [
    (passing_command, 0, '= end of {} ='),
    (passing_command_with_context, 0, '= end of {} ='),
    (failing_command, -1, '= end of {} (exit code: -1) ='),
    (failing_handled_command, 2, '= end of {} (exit code: 2) ='),
    (exited_command, 3, '= end of {} (exit code: 3) ='),
    (aborted_command, 1, '= end of {} (exit code: 1) ='),
    (default_exit_command, 1, '= end of {} (exit code: 1) ='),
    (custom_exit_command, 5, '= end of {} (exit code: 5) ='),
    (syntax_error_command, -1, '= end of {} (exit code: -1) ='),
])
def test_simple(runner, command, exit_code, end_template):
    result = runner.invoke(command)
    assert result.exit_code == exit_code
    assert '= ' + command.name + ' =' in result.output
    assert end_template.format(command.name) in result.output
