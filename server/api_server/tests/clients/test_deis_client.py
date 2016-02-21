from api_server.clients.deis_client import DeisClient


def test_simple(deis_url):
    client = DeisClient(deis_url)
    assert client.deis_url == deis_url
