import click
import pytest

from tigerhost import exit_codes

from deploy.utils import click_utils


@click.command()
def dummy():
    value = click_utils.prompt_choices(['choice 1', 'choice 2', 'choice 3'])
    click.echo('Choice is {}'.format(value + 1))


@pytest.mark.parametrize('choice', range(1, 4))
def test_choice_valid(choice, runner):
    result = runner.invoke(dummy, input='{}\n'.format(choice))
    assert result.exit_code == exit_codes.SUCCESS
    assert 'Choice is {}'.format(choice) in result.output


@pytest.mark.parametrize('choice', [0, 4])
def test_choice_invalid(choice, runner):
    result = runner.invoke(dummy, input='{}\n'.format(choice))
    assert result.exit_code == exit_codes.ABORT
    assert 'Invalid choice' in result.output
