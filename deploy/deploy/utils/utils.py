import boto3
import os
import random
import string
import sys


def random_string(length, allowed_chars=string.ascii_letters + string.digits):
    rand = random.SystemRandom()
    return ''.join(rand.choice(allowed_chars) for _ in range(length))


def parse_shell_for_exports(text):
    """Parses a shell script and extracts all of its exports.

    :param str text: The shell script

    :rtype: dict
    :returns: for example,

        export VAR1=value1
        ...
        export VAR2="value2"

        will return: {

            'VAR1': 'value1',

            'VAR2': 'value2',

        }
    """
    lines = [x for x in text.split('\n') if x.startswith('export ')]
    lines = [x[len('export '):] for x in lines]
    env = dict()
    for l in lines:
        key, value = l.split('=', 1)
        value = value.split('#', 1)[0].strip().strip('"').strip("'")
        env[key] = value
    return env


def set_aws_security_group_ingress_rule(group_name, fromPort, toPort, cidrIp):
    """Add an ingress rule to a security group.

    :param str group_name:
    :param int fromPort:
    :param int toPort:
    :param str cidrIp:
    """
    ec2 = boto3.resource('ec2')
    group = list(ec2.security_groups.filter(
        GroupNames=[group_name]).limit(1))[0]
    found = False
    for perm in group.ip_permissions:
        if perm['FromPort'] != fromPort or perm['ToPort'] != toPort or perm['IpProtocol'] != 'tcp':
            continue
        for ip in perm['IpRanges']:
            if ip['CidrIp'] == cidrIp:
                found = True
    if not found:
        group.authorize_ingress(
            IpProtocol='tcp', FromPort=0, ToPort=65535, CidrIp='0.0.0.0/0')


def which(cmd, mode=os.F_OK | os.X_OK, path=None):
    """Given a command, mode, and a PATH string, return the path which
    conforms to the given mode on the PATH, or None if there is no such
    file.

    `mode` defaults to os.F_OK | os.X_OK. `path` defaults to the result
    of os.environ.get("PATH"), or can be overridden with a custom search
    path.

    This code is taken from python 3's shutil:
    https://hg.python.org/cpython/file/6860263c05b3/Lib/shutil.py#l1068
    """
    # Check that a given file can be accessed with the correct mode.
    # Additionally check that `file` is not a directory, as on Windows
    # directories pass the os.access check.
    def _access_check(fn, mode):
        return (os.path.exists(fn) and os.access(fn, mode) and not os.path.isdir(fn))

    # If we're given a path with a directory part, look it up directly rather
    # than referring to PATH directories. This includes checking relative to the
    # current directory, e.g. ./script
    if os.path.dirname(cmd):
        if _access_check(cmd, mode):
            return cmd
        return None

    if path is None:
        path = os.environ.get("PATH", os.defpath)
    if not path:
        return None
    path = path.split(os.pathsep)

    if sys.platform == "win32":
        # The current directory takes precedence on Windows.
        if os.curdir not in path:
            path.insert(0, os.curdir)

        # PATHEXT is necessary to check on Windows.
        pathext = os.environ.get("PATHEXT", "").split(os.pathsep)
        # See if the given file matches any of the expected path extensions.
        # This will allow us to short circuit when given "python.exe".
        # If it does match, only test that one, otherwise we have to try
        # others.
        if any(cmd.lower().endswith(ext.lower()) for ext in pathext):
            files = [cmd]
        else:
            files = [cmd + ext for ext in pathext]
    else:
        # On other platforms you don't have things like PATHEXT to tell you
        # what file suffixes are executable, so just pass on cmd as-is.
        files = [cmd]

    seen = set()
    for dir in path:
        normdir = os.path.normcase(dir)
        if normdir not in seen:
            seen.add(normdir)
            for thefile in files:
                name = os.path.join(dir, thefile)
                if _access_check(name, mode):
                    return name
    return None
