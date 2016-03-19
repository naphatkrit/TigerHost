import pytest

from api_server.utils import git_remote


@pytest.mark.parametrize('deis_url,app_id,remote', [
    ('http://deis.local3.deisapp.com', 'app-id',
     'ssh://git@deis.local3.deisapp.com:2222/app-id.git'),
    ('http://deis.local3.deisapp.com:200', 'app-id',
     'ssh://git@deis.local3.deisapp.com:2222/app-id.git'),
    ('https://deis.local3.deisapp.com', 'app-id',
     'ssh://git@deis.local3.deisapp.com:2222/app-id.git'),
    ('ssh://somethingelse@deis.local3.deisapp.com', 'app-id',
     'ssh://git@deis.local3.deisapp.com:2222/app-id.git'),
    ('ssh://somethingelse:password@deis.local3.deisapp.com',
     'app-id', 'ssh://git@deis.local3.deisapp.com:2222/app-id.git'),
])
def test_git_remote(deis_url, app_id, remote):
    assert git_remote(deis_url, app_id) == remote
