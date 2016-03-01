import pytest


@pytest.mark.django_db
def test_GET(client, http_headers, user):
    resp = client.get('/api/v1/providers/', **http_headers)
    assert resp.status_code == 200
    assert resp.json()['results'] == user.profile.get_providers()
