import random
import string


def random_string(length, allowed_chars=string.ascii_letters + string.digits):
    rand = random.SystemRandom()
    return ''.join(rand.choice(allowed_chars) for _ in range(length))


def parse_shell_for_exports(text):
    """Parses a shell script and extracts all of its exports.

    @type text: str
        The shell script

    @rtype: dict
        for example,

        export VAR1=value1
        ...
        export VAR2="value2"

        will return:

        {
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
