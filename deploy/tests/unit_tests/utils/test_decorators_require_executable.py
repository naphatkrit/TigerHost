import click
import mock

from tigerhost import exit_codes

from deploy.utils.decorators import require_executable


@click.command()
@require_executable('test')
def dummy():
    pass


def test_require_executable_exists(runner):
    with mock.patch('deploy.utils.utils.which') as mocked:
        mocked.return_value = 'test'
        result = runner.invoke(dummy)
    assert result.exit_code == exit_codes.SUCCESS


def test_require_executable_does_not_exist(runner):
    with mock.patch('deploy.utils.utils.which') as mocked:
        mocked.return_value = None
        result = runner.invoke(dummy)
    assert result.exit_code == exit_codes.OTHER_FAILURE
