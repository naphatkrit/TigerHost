import os
import pytest

from tigerhost import settings
from tigerhost import private_dir


def test_ensure_private_dir_exists():
    assert not os.path.exists(private_dir.private_dir_path(settings.APP_NAME))
    private_dir.ensure_private_dir_exists(settings.APP_NAME)
    assert os.path.exists(private_dir.private_dir_path(settings.APP_NAME))
    private_dir.ensure_private_dir_exists(settings.APP_NAME)
    assert os.path.exists(private_dir.private_dir_path(settings.APP_NAME))


def test_ensure_private_dir_exists_conflict():
    assert not os.path.exists(private_dir.private_dir_path(settings.APP_NAME))
    assert not os.system('touch {}'.format(private_dir.private_dir_path(settings.APP_NAME)))
    with pytest.raises(private_dir.PrivateDirConflictError):
        private_dir.ensure_private_dir_exists(settings.APP_NAME)
