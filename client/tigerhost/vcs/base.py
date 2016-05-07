"""
This module is inspired by the open-sourced project Changes:
https://github.com/dropbox/changes
"""
from __future__ import absolute_import

import os
import os.path

from contextlib import contextmanager
from subprocess32 import Popen, PIPE, check_call
from temp_utils import contextmanagers


class CommandError(Exception):
    """An exception when a git command resulted in an error"""

    def __init__(self, cmd, retcode, stdout, stderr):
        self.cmd = cmd
        self.retcode = retcode
        self.stdout = stdout
        self.stderr = stderr

    def __unicode__(self):
        return '%s returned %d:\nSTDOUT: %r\nSTDERR: %r' % (
            self.cmd, self.retcode, self.stdout, self.stderr)  # pragma: no cover

    def __str__(self):
        return self.__unicode__().encode('utf-8')  # pragma: no cover


class Vcs(object):

    def __init__(self, path=None):
        """Initialize a new Vcs object for a repository located at `path`.
        If `path` is `None`, then `get_working_directory` is used to identify
        the path.

        :param str path: optional. The path to the repo working directory.
        """
        self.path = None
        if path is None:
            self.path = self.get_working_directory()
        else:
            self.path = path
        assert self.exists()

    def run(self, *args, **kwargs):
        if self.path is not None:
            # only None when called in the __init__ function
            kwargs.setdefault('cwd', self.path)

        # NOTE if we do want to make a copy of environmental variables,
        # we must remove GIT_WORK_TREE
        kwargs['env'] = {}
        kwargs['stdout'] = PIPE
        kwargs['stderr'] = PIPE

        proc = Popen(args, **kwargs)
        (stdout, stderr) = proc.communicate()
        if proc.returncode != 0:
            raise CommandError(args[0], proc.returncode, stdout, stderr)
        return stdout

    def exists(self):
        """Check if the working directory exists

        :rtype: bool
        :returns: True if the working directory exists
        """
        return os.path.exists(self.path)

    def get_working_directory(self):
        """Get the working directory for this repo.

        :rtype: str
        :returns: the path to the working directory

        :raises tigerhost.vcs.base.CommandError:
        """
        raise NotImplementedError  # pragma: no cover

    def install_hook(self, hook_name, hook_content):
        """Install the repository hook for this repo.

        :param str hook_name: the name of the hook (pre-receive, etc.)
        :param str hook_content: the content of the script
        """
        raise NotImplementedError  # pragma: no cover

    def remove_ignored_files(self):
        """Remove files ignored by the repository
        """
        raise NotImplementedError  # pragma: no cover

    def remove_unstaged_files(self):
        """Remove all unstaged files. This does NOT remove ignored files.

        TODO this may be specific to git?
        """
        raise NotImplementedError  # pragma: no cover

    def clear(self, target_commit):
        """Resets the repository to the target commit, removing any staged,
        unstaged, and untracked files.

        :param str target_commit: the commit ID

        :raises tigerhost.vcs.base.CommandError: if the commit does not exist
        """
        raise NotImplementedError  # pragma: no cover

    def private_dir(self):
        """Get the private directory associated with this repo, but untracked
        by the repo.

        :rtype: str
        :returns: absolute path
        """
        raise NotImplementedError  # pragma: no cover

    def repository_dir(self):
        """Get the directory used by the VCS to store repository info.

        e.g. .git for git

        :rtype: str
        :returns: absolute path
        """
        raise NotImplementedError  # pragma: no cover

    def get_signature(self, base_commit=None):
        """Get the signature of the current state of the repository

        :param str base_commit: the base commit ('HEAD', sha, etc.)

        :rtype: str
        :returns: a unique signature for the current state of the repo
        """
        raise NotImplementedError  # pragma: no cover

    def ignore_patterns_file(self):
        """The ignore patterns file for this repo type.

        e.g. .gitignore for git

        :rtype: str
        :returns: file name
        """
        raise NotImplementedError  # pragma: no cover

    def path_is_ignored(self, path):
        """Given a path, check if the path would be ignored.

        :rtype: bool
        :returns: True if the path would be ignored
        """
        raise NotImplementedError  # pragma: no cover

    def get_ignored_files(self):
        """Returns the list of files being ignored in this repository.

        Note that file names, not directories, are returned.

        So, we will get the following:

        a/b.txt
        a/c.txt

        instead of just:

        a/

        :rtype: list
        :returns: list of ignored files. The paths are relative to the repo.
        """
        raise NotImplementedError  # pragma: no cover

    def add_remote(self, name, url):
        """Add a new remote to this repository.

        :param str name: remote name
        :param str url: remote URL
        """
        raise NotImplementedError  # pragma: no cover

    def remove_remote(self, name):
        """Remove a remote from this repository.

        :param str name: remote name
        """
        raise NotImplementedError  # pragma: no cover

    def get_remotes(self):
        """Returns all the remotes in this repository.

        :rtype: dict
        :returns: mapping from remote name to remote URLs (str to str)
        """
        raise NotImplementedError  # pragma: no cover

    @contextmanager
    def temp_copy(self):
        """Yields a new Vcs object that represents a temporary, disposable
        copy of the current repository. The copy is deleted at the end
        of the context.

        The following are not copied:
        - ignored files
        - tigerhost private directory (.git/tigerhost for git)

        Yields:
            Vcs
        """
        with contextmanagers.temp_dir() as temp_dir:
            temp_root_path = os.path.join(temp_dir, 'root')
            path = os.path.join(self.path, '')  # adds trailing slash
            check_call(['rsync', '-r', "--exclude={}".format(self.private_dir()), "--filter=dir-merge,- {}".format(
                self.ignore_patterns_file()), path, temp_root_path])
            copy = self.__class__(path=temp_root_path)
            yield copy
