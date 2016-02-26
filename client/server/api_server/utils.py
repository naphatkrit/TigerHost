import urlparse


def git_remote(deis_url, app_id):
    """Return the corresponding git remote for this app ID. Uses
    the hostname from ``deis_url``

    @type deis_url: str
    @type app_id: str

    @rtype: str
    """
    url = urlparse.urlparse(deis_url)
    return 'ssh://git@{hostname}:2222/{app_id}.git'.format(
        hostname=url.hostname,
        app_id=app_id
    )
