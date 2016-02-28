from tigerhost.entry import entry
from tigerhost.user import load_user


def test_user_info_success(runner, fake_api_client, saved_user):
    user = load_user()
    result = runner.invoke(entry, ['user:info'])
    assert result.exit_code == 0
    assert user.username in result.output
    assert user.api_key in result.output


def test_user_info_failure(runner, fake_api_client):
    result = runner.invoke(entry, ['user:info'])
    assert result.exit_code == 2


def test_logout(runner, fake_api_client, saved_user):
    result = runner.invoke(entry, ['logout'])
    assert result.exit_code == 0
    result = runner.invoke(entry, ['user:info'])
    assert result.exit_code == 2
    result = runner.invoke(entry, ['logout'])
    assert result.exit_code == 2
