import os
import pytest

from tigerhostctl.utils.path_utils import canonical_path


@pytest.mark.parametrize('short,full', [
    ('~', os.path.expanduser('~')),
    ('~/.', os.path.expanduser('~')),
    ('./testing', os.path.abspath('testing')),
    ('/./././ab/../././ab', '/ab'),
])
def test_canonical_path(short, full):
    assert canonical_path(short) == full
