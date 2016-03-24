import click
import pytest

from tigerhost.vcs.git import GitVcs
from tigerhost.utils import decorators


@click.command()
@decorators.store_app
@click.pass_context
@decorators.print_markers
def command_with_context(ctx):
    click.echo(ctx.obj['app'])


@click.command()
@decorators.print_markers
@decorators.store_vcs
@decorators.store_app
@click.pass_context
@decorators.print_markers
def command_with_context_and_vcs1(ctx):
    click.echo(ctx.obj['app'])


@click.command()
@decorators.store_app
@decorators.store_vcs
@click.pass_context
@decorators.print_markers
def command_with_context_and_vcs2(ctx):
    click.echo(ctx.obj['app'])


@pytest.mark.parametrize('command', [
    command_with_context,
    command_with_context_and_vcs1,
    command_with_context_and_vcs2,
])
def test_no_git(runner, command):
    result = runner.invoke(command)
    assert result.exit_code == 2

    result = runner.invoke(command, ['--app', 'a-1'])
    assert result.exit_code == 0
    assert 'a-1' in result.output


@pytest.mark.parametrize('command', [
    command_with_context,
    command_with_context_and_vcs1,
    command_with_context_and_vcs2,
])
def test_with_git(runner, make_git_repo, command):
    result = runner.invoke(command)
    assert result.exit_code == 2

    result = runner.invoke(command, ['--app', 'a-1'])
    assert result.exit_code == 0
    assert 'a-1' in result.output

    git = GitVcs()
    git.add_remote('tigerhost', 'a-2')

    result = runner.invoke(command)
    assert result.exit_code == 0
    assert 'a-2' in result.output

    result = runner.invoke(command, ['--app', 'a-1'])
    assert result.exit_code == 0
    assert 'a-1' in result.output
