import hashlib
import os
import stat

from subprocess32 import Popen, PIPE

from tigerhost import settings
from tigerhost.vcs.base import CommandError, Vcs


class GitVcs(Vcs):
    binary_path = 'git'

    def __init__(self, path=None):
        super(GitVcs, self).__init__(path)
        private_dir = self.private_dir()
        if not os.path.exists(private_dir):
            os.makedirs(private_dir)

    @classmethod
    def clone(cls, remote_url, path):
        """Clone the remote and return a GitVcs object pointed at the new repo.

        Args:
            remote_url (str)
            path (str) - path to clone to

        Returns:
            GitVcs

        Raises:
            CommandError
        """
        args = ['git', 'clone', '--recursive', remote_url, path]
        proc = Popen(args, stdout=PIPE, stderr=PIPE)
        (stdout, stderr) = proc.communicate()
        if proc.returncode != 0:
            raise CommandError(args[0], proc.returncode, stdout, stderr)
        return cls(path=path)

    def get_working_directory(self):
        """Get the working directory for this repo.

        This is available as a class method as it is usually needed to
        initialize the VCS object itself.

        Args:
            cls (class object): The class

        Returns:
            str - the path to the working directory

        Raises:
            CommandError
        """
        return self.run('rev-parse', '--show-toplevel').strip()

    def run(self, *cmd, **kwargs):
        cmd = [self.binary_path] + list(cmd)
        return super(GitVcs, self).run(*cmd, **kwargs)

    def remove_ignored_files(self):
        """Remove files ignored by the repository
        """
        self.run('clean', '-fdX')

    def remove_unstaged_files(self):
        """Remove all unstaged files. This does NOT remove ignored files.

        TODO this may be specific to git?
        """
        self.run('clean', '-fd')  # remove untracked files
        self.run('checkout', self.path)  # revert changes to staged version

    def clear(self, target_commit):
        """Resets the repository to the target commit, removing any staged,
        unstaged, and untracked files.

        Args:
            target_commit (str): the commit ID
        Raises:
            CommandError - if the commit does not exist
        """
        self.run('reset', '--hard', target_commit)
        self.run('clean', '-fd')

    def private_dir(self):
        """Get the private directory associated with this repo, but untracked
        by the repo.

        Returns:
            str - absolute path
        """
        return os.path.join(self.repository_dir(), settings.APP_NAME)

    def repository_dir(self):
        """Get the directory used by the VCS to store repository info.

        e.g. .git for git

        Returns:
            str - absolute path
        """
        return os.path.join(self.path, '.git')

    def get_signature(self, base_commit=None):
        """Get the signature of the current state of the repository

        TODO right now `get_signature` is an effectful process in that
        it adds all untracked file to staging. This is the only way to get
        accruate diff on new files. This is ok because we only use it on a
        disposable copy of the repo.

        Args:
            base_commit - the base commit ('HEAD', sha, etc.)

        Returns:
            str
        """
        if base_commit is None:
            base_commit = 'HEAD'
        self.run('add', '-A', self.path)
        sha = self.run('rev-parse', '--verify', base_commit).strip()
        diff = self.run('diff', sha).strip()
        if len(diff) == 0:
            try:
                return self.get_signature(base_commit + '~1')
            except CommandError:
                pass
        h = hashlib.sha1()
        h.update(sha)
        h.update(diff)
        return h.hexdigest()

    def install_hook(self, hook_name, hook_content):
        """Install the repository hook for this repo.

        Args:
            hook_name (str)
            hook_content (str)
        """
        hook_path = os.path.join(self.path, '.git/hooks', hook_name)
        with open(hook_path, 'w') as f:
            f.write(hook_content)
        os.chmod(hook_path, stat.S_IEXEC | stat.S_IREAD | stat.S_IWRITE)

    def get_ignored_files(self):
        """Returns the list of files being ignored in this repository.

        Note that file names, not directories, are returned.

        So, we will get the following:

        a/b.txt
        a/c.txt

        instead of just:

        a/

        Returns:
            List[str] - list of ignored files. The paths are absolute.
        """
        return [os.path.join(self.path, p) for p in
                self.run('ls-files', '--ignored', '--exclude-standard',
                         '--others').strip().split()
                ]

    def ignore_patterns_file(self):
        """The ignore patterns file for this repo type.

        e.g. .gitignore for git

        Returns:
            str - file name
        """
        return '.gitignore'

    def add_remote(self, name, url):
        """Add a new remote to this repository.

        Args:
            name (str)
            url (str)
        """
        self.run('remote', 'add', name, url)

    def remove_remote(self, name):
        """Remove a remote from this repository.

        Args:
            name (str)
        """
        self.run('remote', 'remove', name)

    def get_remotes(self):
        """Returns all the remotes in this repository.

        Returns:
            Dict[str:str] - mapping from remote name to remote URLs
        """
        remotes = self.run('remote', '--verbose').strip().split('\n')
        if remotes == ['']:
            return {}
        remotes = [x.split() for x in remotes]
        answer = {}
        for name, url, _ in remotes:
            # note that each name has a duplicate (fetch vs. push)
            answer[name] = url
        return answer

    def path_is_ignored(self, path):
        """Given a path, check if the path would be ignored.

        Returns:
            boolean
        """
        try:
            self.run('check-ignore', '--quiet', path)
        except CommandError as e:
            if e.retcode == 1:
                # path is ignored
                return False
            else:
                # fatal error
                raise e
        return True
