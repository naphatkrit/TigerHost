import mock
import os
import pytest

from temp_utils import contextmanagers

from tigerhost.vcs.base import Vcs


class DummyVcs(Vcs):
    def get_working_directory(self):
        return os.getcwd()

    def private_dir(self):
        return os.path.join(self.path, '.dummy/tigerhost')

    def ignore_patterns_file(self):
        return '.dummyignore'


@pytest.yield_fixture(scope='function')
def temp_path():
    with contextmanagers.temp_dir() as temp:
        with contextmanagers.chdir(temp):
            yield temp


def test_init_with_path():
    path = '/dummy'
    with mock.patch('os.path.exists') as mocked:
        mocked.return_value = True
        vcs = Vcs(path=path)
        assert vcs.path == path

        mocked.return_value = False
        with pytest.raises(AssertionError):
            Vcs(path=path)


def test_init_without_path():
    path = '/dummy'
    with mock.patch('tigerhost.vcs.base.Vcs.get_working_directory') as mocked:
        mocked.return_value = path
        with mock.patch('os.path.exists') as path_mocked:
            path_mocked.return_value = True
            vcs = Vcs()
            assert vcs.path == path

            path_mocked.return_value = False
            with pytest.raises(AssertionError):
                Vcs()


def test_temp_copy(temp_path):
    vcs = DummyVcs()
    assert not os.system("echo '*.txt' > {}".format(vcs.ignore_patterns_file()))
    assert not os.system("touch a.txt b")
    with vcs.temp_copy() as copy:
        assert isinstance(copy, DummyVcs)
        assert copy.path != vcs.path
        assert os.path.exists(copy.path)
        assert os.path.exists(os.path.join(copy.path, copy.ignore_patterns_file()))
        assert not os.path.exists(os.path.join(copy.path, 'a.txt'))
        assert os.path.exists(os.path.join(copy.path, 'b'))
    assert not os.path.exists(copy.path)
