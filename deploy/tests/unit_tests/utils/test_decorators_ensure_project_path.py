import click
import mock
import os

from click_extensions import exit_codes

from deploy.utils import decorators, path_utils
from deploy.project import get_project_path, save_project_path, default_project_path


@click.command()
@decorators.ensure_project_path
def dummy():
    pass


def test_without_project_path_default_normal(runner, fake_git_remote):
    assert get_project_path() is None
    with mock.patch('deploy.settings.PROJECT_REMOTE', new=fake_git_remote):
        result = runner.invoke(dummy, input='1\n')
    assert result.exit_code == exit_codes.SUCCESS
    assert get_project_path() == path_utils.canonical_path(default_project_path())


def test_without_project_path_default_exists_file(runner, fake_git_remote):
    assert get_project_path() is None
    assert not os.system('touch {}'.format(default_project_path()))
    with mock.patch('deploy.settings.PROJECT_REMOTE', new=fake_git_remote):
        result = runner.invoke(dummy, input='1\n\n')
    assert result.exit_code == exit_codes.SUCCESS
    assert get_project_path() == path_utils.canonical_path(default_project_path())


def test_without_project_path_default_exists_dir(runner, fake_git_remote):
    assert get_project_path() is None
    assert not os.system('mkdir {}'.format(default_project_path()))
    with mock.patch('deploy.settings.PROJECT_REMOTE', new=fake_git_remote):
        result = runner.invoke(dummy, input='1\n\n')
    assert result.exit_code == exit_codes.SUCCESS
    assert get_project_path() == path_utils.canonical_path(default_project_path())


def test_without_project_path_default_exists_abort(runner, fake_git_remote):
    assert get_project_path() is None
    assert not os.system('mkdir {}'.format(default_project_path()))
    with mock.patch('deploy.settings.PROJECT_REMOTE', new=fake_git_remote):
        result = runner.invoke(dummy, input='1\nn\n')
    assert result.exit_code == exit_codes.ABORT
    assert get_project_path() is None


def test_without_project_path_normal(runner):
    assert get_project_path() is None
    result = runner.invoke(dummy, input='2\n.\n\n')
    assert result.exit_code == exit_codes.SUCCESS
    assert get_project_path() == path_utils.canonical_path('.')


def test_without_project_path_nonexist(runner):
    assert get_project_path() is None
    result = runner.invoke(dummy, input='2\n/doesnotexist\n\n')
    assert result.exit_code == exit_codes.OTHER_FAILURE
    assert get_project_path() is None


def test_without_project_path_not_confirmed(runner):
    assert get_project_path() is None
    result = runner.invoke(dummy, input='2\n.\nn\n')
    assert result.exit_code == exit_codes.ABORT
    assert get_project_path() is None


def test_path_already_exists(runner):
    assert get_project_path() is None
    save_project_path('.')
    result = runner.invoke(dummy)
    assert result.exit_code == exit_codes.SUCCESS
    assert get_project_path() == path_utils.canonical_path('.')
