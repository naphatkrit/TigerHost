from tigerhost.entry import entry


def test_list_domains(runner, saved_user, fake_api_client):
    """
    @type runner: click.testing.CliRunner
    @type fake_api_client: mock.Mock
    """
    domains = ['a.example.com', 'b.example.com']
    fake_api_client.get_application_domains.return_value = domains
    result = runner.invoke(entry, ['domains', '--app', 'app'])
    assert result.exit_code == 0
    for x in domains:
        assert x in result.output
    fake_api_client.get_application_domains.assert_called_once_with('app')


def test_add_domain(runner, saved_user, fake_api_client):
    """
    @type runner: click.testing.CliRunner
    @type fake_api_client: mock.Mock
    """
    domain = 'a.example.com'
    result = runner.invoke(entry, ['domains:add', '--app', 'app', domain])
    assert result.exit_code == 0
    assert domain in result.output
    fake_api_client.add_application_domain.assert_called_once_with(
        'app', domain)


def test_remove_domain(runner, saved_user, fake_api_client):
    """
    @type runner: click.testing.CliRunner
    @type fake_api_client: mock.Mock
    """
    domain = 'a.example.com'
    result = runner.invoke(entry, ['domains:remove', '--app', 'app', domain])
    assert result.exit_code == 0
    assert domain in result.output
    fake_api_client.remove_application_domain.assert_called_once_with(
        'app', domain)
