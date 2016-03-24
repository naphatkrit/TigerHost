from tigerhost.entry import entry

from tigerhost.vcs.git import GitVcs


def test_git_remotes(runner, make_app, app_id):
    """
    @type runner: click.testing.CliRunner
    """
    remote = 'tigerhost2'
    result = runner.invoke(entry, ['git:remote', '--app', app_id, '--remote', remote])
    assert result.exit_code == 0
    assert remote in result.output

    git = GitVcs()
    remotes = git.get_remotes()
    assert remotes[remote] == remotes['tigerhost']
