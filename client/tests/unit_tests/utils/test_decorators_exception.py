import click
import pytest

from tigerhost.utils import decorators


class ErrorA(Exception):
    pass


class ErrorB(Exception):
    pass


@click.command()
@decorators.catch_exception(ErrorA)
def throw_A():
    raise ErrorA


@click.command()
@decorators.catch_exception(ErrorA)
def throw_B():
    raise ErrorB


@click.command()
@click.pass_context
@decorators.catch_exception(ErrorA)
def throw_A_with_context(ctx):
    raise ErrorA


@click.command()
@click.pass_context
@decorators.catch_exception(ErrorA)
def throw_B_with_context(ctx):
    raise ErrorB


@pytest.mark.parametrize('command,exit_code', [
    (throw_A, 1),
    (throw_B, -1),
])
def test_simple(runner, command, exit_code):
    result = runner.invoke(command)
    assert result.exit_code == exit_code
