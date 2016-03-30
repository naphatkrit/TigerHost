from tigerhostctl import user_config


def test_user_config():
    assert user_config.get('key1') is None
    assert user_config.get('key1', False) is False
    user_config.set('key1', 'test')
    assert user_config.get('key1') == 'test'
