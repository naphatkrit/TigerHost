import os

from deploy.secret_dir import ensure_secret_dir_exists, secret_dir_path


def test_secret_dir_exists():
    path = secret_dir_path()
    assert not os.path.exists(path)
    ensure_secret_dir_exists()
    assert os.path.exists(path)
    ensure_secret_dir_exists()
    assert os.path.exists(path)
