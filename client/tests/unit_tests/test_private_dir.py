import os
import pytest

from tigerhost import private_dir


def test_ensure_private_dir_exists():
    assert not os.path.exists(private_dir.private_dir_path())
    private_dir.ensure_private_dir_exists()
    assert os.path.exists(private_dir.private_dir_path())
    private_dir.ensure_private_dir_exists()
    assert os.path.exists(private_dir.private_dir_path())


def test_ensure_private_dir_exists_conflict():
    assert not os.path.exists(private_dir.private_dir_path())
    assert not os.system('touch {}'.format(private_dir.private_dir_path()))
    with pytest.raises(private_dir.PrivateDirConflictError):
        private_dir.ensure_private_dir_exists()
