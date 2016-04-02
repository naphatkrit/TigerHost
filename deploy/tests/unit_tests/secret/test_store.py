from deploy.secret import store


def test_store():
    assert store.get('key1') is None
    assert store.get('key1', False) is False
    store.set('key1', 'test')
    assert store.get('key1') == 'test'
