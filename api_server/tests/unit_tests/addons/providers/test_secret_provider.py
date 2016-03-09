from api_server.addons.providers.secret_provider import SecretAddonProvider


def test_wait_for_provision():
    provider = SecretAddonProvider()
    result = provider.wait_for_provision(None)
    assert len(result['config']['SECRET_KEY']) == 100


def test_begin_provision():
    provider = SecretAddonProvider()
    result = provider.begin_provision(None)
    assert 'uuid' in result
    assert 'message' in result

def test_deprovision():
    provider = SecretAddonProvider()
    result = provider.deprovision(None)
    assert 'message' in result
