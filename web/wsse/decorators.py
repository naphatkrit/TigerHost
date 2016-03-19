from functools import wraps

from django.contrib import auth
from django.http import HttpResponse
from django.utils.decorators import available_attrs

from wsse.utils import parse_wsse_header


def check_wsse_token(view_func):
    """A decorator that, if the user is not already authenticated, attempts
    to authenticate the user using wsse token.

    If the user is already authenticated, this doesn't do anything.

    If the user is not successfully authenticated, this returns a HTTP 401
    """
    def create_401_response():
        response = HttpResponse('Unauthorized', status=401)
        response['WWW-Authenticate'] = 'WSSE realm="api", profile="UsernameToken"'
        return response

    @wraps(view_func, assigned=available_attrs(view_func))
    def wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated():
            return view_func(request, *args, **kwargs)

        if 'HTTP_X_WSSE' not in request.META:
            return create_401_response()

        wsse_header = request.META['HTTP_X_WSSE']
        try:
            username, digest, nonce, timestamp = parse_wsse_header(
                wsse_header)
        except ValueError:
            return create_401_response()

        user = auth.authenticate(
            username=username, digest=digest, nonce=nonce, timestamp=timestamp)
        if user is None:
            return create_401_response()
        auth.login(request, user)
        return view_func(request, *args, **kwargs)

    return wrapped_view
