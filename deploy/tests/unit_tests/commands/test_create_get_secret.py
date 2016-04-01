import click

from tigerhost import exit_codes

from deploy.commands.create import _get_secret


@click.command()
def dummy():
    secret = _get_secret()
    click.echo('My secret is {}.'.format(secret))


def test_get_secret_generate(runner):
    result = runner.invoke(dummy, input='1\n\n')
    assert result.exit_code == exit_codes.SUCCESS
    secret = [x for x in result.output.split('\n') if x.startswith('Generated secret: ')][0]
    secret = secret[len('Generated secret: '):]
    assert 'My secret is {}.'.format(secret) in result.output


def test_get_secret_input(runner):
    result = runner.invoke(dummy, input='2\nsecret\nsecret\n')
    assert result.exit_code == exit_codes.SUCCESS
    assert 'My secret is secret.' in result.output
