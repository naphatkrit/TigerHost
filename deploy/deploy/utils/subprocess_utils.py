import subprocess32 as subprocess


def check_call_realtime(args):
    """Run command with arguments and yield the output as they come.

    Stderr is piped into stdout.

    :raises subprocess.CalledProcessError: if exit code is non-zero
    """
    p = subprocess.Popen(args, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    while p.poll() is None:
        yield p.stdout.read()
    yield p.stdout.read()
    if p.returncode != 0:
        raise subprocess.CalledProcessError(p.returncode, args)
