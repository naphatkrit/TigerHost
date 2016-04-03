import click
import mock

from tigerhost import exit_codes

from deploy.utils.decorators import require_docker_machine


@click.command()
@require_docker_machine
def dummy():
    pass


def test_require_docker_machine_exists(runner):
    with mock.patch('deploy.utils.utils.which') as mocked:
        mocked.return_value = 'test'
        result = runner.invoke(dummy)
    assert result.exit_code == exit_codes.SUCCESS


def test_require_docker_machine_does_not_exist(runner):
    with mock.patch('deploy.utils.utils.which') as mocked:
        mocked.return_value = None
        result = runner.invoke(dummy)
    assert result.exit_code == exit_codes.OTHER_FAILURE
