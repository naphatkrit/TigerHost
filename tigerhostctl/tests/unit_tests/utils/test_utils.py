import pytest

from tigerhostctl.utils.utils import parse_shell_for_exports


@pytest.mark.parametrize('script,env', [
    ('''
export VAR1='value1'
some other command

# comment here

export VAR2=value2 # comment here

''', {'VAR1': 'value1', 'VAR2': 'value2'}),
    ('''
export VAR1=value1
export VAR1="value2"
''', {'VAR1': 'value2'}),
])
def test_parse_shell_for_exports(script, env):
    assert parse_shell_for_exports(script) == env
