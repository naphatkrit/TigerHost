import click
import subprocess32 as subprocess

from temp_utils import contextmanagers

from deploy.secret import secret_dir


@click.command()
@click.argument('commands', nargs=-1)
@click.pass_context
def secret(ctx, commands):
    """Executes git commands in the secret directory. This literally forwards all the arguments to git.

    tigerhost-deploy secret push origin master

    becomes:

    git push origin master

    in the secret directory.
    """
    with contextmanagers.chdir(secret_dir.secret_dir_path()):
        ret = subprocess.call(['git'] + list(commands))
    ctx.exit(code=ret)
