import pytest


@pytest.mark.django_db
def test_GET(client, http_headers, user, settings):
    resp = client.get('/api/v1/backends/', **http_headers)
    assert resp.status_code == 200
    assert resp.json()['backends'] == user.profile.get_paas_backends()
    assert resp.json()['default'] == settings.DEFAULT_PAAS_BACKEND
