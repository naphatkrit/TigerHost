import click

from tigerhost import exit_codes

from tigerhostctl.utils import decorators, utils
from tigerhostctl.project import get_project_path, save_project_path


@click.command()
@decorators.ensure_project_path
def dummy():
    pass


def test_without_project_path_normal(runner):
    assert get_project_path() is None
    result = runner.invoke(dummy, input='.\n\n')
    assert result.exit_code == exit_codes.SUCCESS
    assert get_project_path() == utils.canonical_path('.')


def test_without_project_path_nonexist(runner):
    assert get_project_path() is None
    result = runner.invoke(dummy, input='/doesnotexist\n\n')
    assert result.exit_code == exit_codes.OTHER_FAILURE
    assert get_project_path() is None


def test_without_project_path_not_confirmed(runner):
    assert get_project_path() is None
    result = runner.invoke(dummy, input='.\nn\n')
    assert result.exit_code == exit_codes.ABORT
    assert get_project_path() is None


def test_without_project_path_already_exists(runner):
    assert get_project_path() is None
    save_project_path('.')
    result = runner.invoke(dummy)
    assert result.exit_code == exit_codes.SUCCESS
    assert get_project_path() == utils.canonical_path('.')
