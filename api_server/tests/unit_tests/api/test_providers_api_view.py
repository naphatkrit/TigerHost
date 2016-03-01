import pytest


@pytest.mark.django_db
def test_GET(client, http_headers, user, settings):
    resp = client.get('/api/v1/providers/', **http_headers)
    assert resp.status_code == 200
    assert resp.json()['providers'] == user.profile.get_providers()
    assert resp.json()['default'] == settings.DEFAULT_PAAS_PROVIDER
