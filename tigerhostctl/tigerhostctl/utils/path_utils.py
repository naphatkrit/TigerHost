import os


def canonical_path(path):
    """Return the canonical path. This expands ~ and resolves
    any symbolic links, and returns the absolute path.

    @type path: str

    @rtype: str
    """
    return os.path.realpath(os.path.expanduser(path))


def ssh_path(name):
    """Return the canonical path to ~/.ssh/{name}

    @rtype: str
    """
    return canonical_path(os.path.join('~/.ssh', name))
