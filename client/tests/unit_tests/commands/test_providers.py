from tigerhost.entry import entry


def test_list_backends(runner, fake_api_client, saved_user):
    backends_info = {
        'backends': ['aws', 'deis'],
        'default': 'aws',
    }
    fake_api_client.get_backends.return_value = backends_info
    result = runner.invoke(entry, ['backends'])
    assert result.exit_code == 0
    for p in backends_info['backends']:
        assert p in result.output
    fake_api_client.get_backends.assert_called_once_with()
