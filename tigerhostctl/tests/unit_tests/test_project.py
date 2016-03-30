import mock
import os

from tigerhost.utils import contextmanagers

from tigerhostctl.project import get_project_path, save_project_path, clone_project, default_project_path


def test_project_path():
    assert get_project_path() is None
    save_project_path('/test/../')
    assert get_project_path() == '/'


def test_clone_project():
    path = default_project_path()
    assert not os.path.exists(path)
    with contextmanagers.temp_dir() as temp_dir:
        with contextmanagers.chdir(temp_dir):
            assert not os.system('git init')
            assert not os.system('touch a && git add . && git commit -m a')
        with mock.patch('tigerhostctl.settings.PROJECT_REMOTE', new=temp_dir):
            clone_project()
    assert os.path.exists(path)
    assert os.path.exists(os.path.join(path, 'a'))
