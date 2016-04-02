import click
import os
import responses

from deploy import settings
from deploy.utils import path_utils
from deploy.utils.decorators import ensure_executable_exists, _install_deisctl, _install_deis


def test_ensure_executable_exists(runner):
    name = 'deis'
    path = path_utils.executable_path(name)

    def install_executable():
        assert not os.path.exists(path)
        assert not os.system('touch {}'.format(path))

    @click.command()
    @ensure_executable_exists(name, install_executable)
    def dummy():
        pass

    assert not os.path.exists(path)
    runner.invoke(dummy)
    assert os.path.exists(path)

    # call again and make sure assertion is not triggered
    runner.invoke(dummy)


@responses.activate
def test_install_deisctl():
    path = path_utils.executable_path('deisctl')
    responses.add(responses.GET, settings.DEISCTL_INSTALL_URL,
                  body='echo $1 > $2/deisctl')
    assert not os.path.exists(path)
    _install_deisctl()
    assert os.path.exists(path)


@responses.activate
def test_install_deis():
    path = path_utils.executable_path('deis')
    responses.add(responses.GET, settings.DEIS_INSTALL_URL,
                  body='echo $1 > deis')
    assert not os.path.exists(path)
    _install_deis()
    assert os.path.exists(path)
