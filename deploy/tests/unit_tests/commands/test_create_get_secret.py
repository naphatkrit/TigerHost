import click

from click_extensions import exit_codes

from deploy.commands.create import _get_secret


@click.command()
def dummy():
    secret = _get_secret()
    click.echo('My secret is {}.'.format(secret))


def test_get_secret_generate(runner):
    result = runner.invoke(dummy, input='1\n\n')
    assert result.exit_code == exit_codes.SUCCESS
