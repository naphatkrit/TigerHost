import mock
import pytest

from django.contrib.auth.models import User, AnonymousUser
from django.http import HttpRequest, HttpResponse

from wsse.decorators import check_wsse_token


@check_wsse_token
def _dummy_view(request):
    assert request.user.is_authenticated()
    return HttpResponse()


@pytest.fixture(scope='function')
def mock_user():
    user = mock.Mock(spec=User)
    user.is_authenticated.return_value = True
    return user


@pytest.fixture(scope='function')
def mock_request():
    request = mock.Mock(spec=HttpRequest)
    request.user = AnonymousUser()
    request.META = {}
    request.META['HTTP_X_WSSE'] = '''UsernameToken Username="bob", PasswordDigest="quR/EWLAV4xLf9Zqyw4pDmfV9OY=", Nonce="d36e316282959a9ed4c89851497a717f", Created="2003-12-15T14:43:07Z"'''
    return request


def mock_login(request, user):
    request.user = user


def test_check_wsse_token_success(mock_request, mock_user):
    with mock.patch('django.contrib.auth.authenticate') as mock_authenticate, mock.patch('django.contrib.auth.login', new=mock_login):
        mock_authenticate.return_value = mock_user
        response = _dummy_view(mock_request)
    assert response.status_code == 200


def test_check_wsse_token_success_pre_authenticated(mock_request, mock_user):
    mock_request.user = mock_user
    response = _dummy_view(mock_request)
    assert response.status_code == 200


def test_check_wsse_token_no_wsse_header(mock_request, mock_user):
    mock_request.META.pop('HTTP_X_WSSE', None)
    with mock.patch('django.contrib.auth.authenticate') as mock_authenticate, mock.patch('django.contrib.auth.login', new=mock_login):
        mock_authenticate.return_value = mock_user
        response = _dummy_view(mock_request)
    assert response.status_code == 401
    assert response[
        'WWW-Authenticate'] == 'WSSE realm="api", profile="UsernameToken"'


def test_check_wsse_token_invalid_wsse_header(mock_request, mock_user):
    with mock.patch('django.contrib.auth.authenticate') as mock_authenticate, mock.patch('django.contrib.auth.login', new=mock_login), mock.patch('wsse.decorators.parse_wsse_header') as mock_parse:
        mock_parse.side_effect = ValueError
        mock_authenticate.return_value = mock_user
        response = _dummy_view(mock_request)
    assert response.status_code == 401
    assert response[
        'WWW-Authenticate'] == 'WSSE realm="api", profile="UsernameToken"'


def test_check_wsse_token_not_authenticated(mock_request, mock_user):
    with mock.patch('django.contrib.auth.authenticate') as mock_authenticate, mock.patch('django.contrib.auth.login', new=mock_login):
        mock_authenticate.return_value = None
        response = _dummy_view(mock_request)
    assert response.status_code == 401
    assert response[
        'WWW-Authenticate'] == 'WSSE realm="api", profile="UsernameToken"'
