import os
import shutil
import tempfile

from contextlib import contextmanager


@contextmanager
def chdir(path):
    """Change the working directory to `path` for the duration of this context
    manager.

    Args:
        path (str)
    """
    cur_cwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(cur_cwd)


@contextmanager
def temp_dir():
    """Create a temporary folder for the duration of this context manager,
    deleting it afterwards.

    Yields:
        str - path to the temporary folder
    """
    path = tempfile.mkdtemp()
    try:
        yield path
    finally:
        shutil.rmtree(path)


@contextmanager
def temp_file():
    """Create a temporary file for the duration of this context manager,
    deleting it afterwards.

    Yields:
        str - path to the file
    """
    fd, path = tempfile.mkstemp()
    os.close(fd)
    try:
        yield path
    finally:
        os.remove(path)
