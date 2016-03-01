from tigerhost.entry import entry


def test_list_providers(runner, fake_api_client, saved_user):
    providers_info = {
        'providers': ['aws', 'deis'],
        'default': 'aws',
    }
    fake_api_client.get_providers.return_value = providers_info
    result = runner.invoke(entry, ['providers'])
    assert result.exit_code == 0
    for p in providers_info['providers']:
        assert p in result.output
    fake_api_client.get_providers.assert_called_once_with()
