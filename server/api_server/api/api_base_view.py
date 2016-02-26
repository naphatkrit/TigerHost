from functools import wraps

from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.utils.decorators import available_attrs, method_decorator
from django.views.generic import View

from api_server.clients.deis_client_errors import DeisClientResponseError, DeisClientError, DeisClientTimeoutError
from api_server.clients.deis_client import DeisClient


def _handle_deis_client_response_error(f):
    @wraps(f, assigned=available_attrs(f))
    def wrapped_view(request, *args, **kwargs):
        try:
            return f(request, *args, **kwargs)
        except DeisClientResponseError as e:
            return JsonResponse(e.response.json(), status=e.response.status_code)
    return wrapped_view


def _handle_error(exception, status, message=None):
    def decorator(f):
        @wraps(f, assigned=available_attrs(f))
        def wrapped_view(request, *args, **kwargs):
            try:
                return f(request, *args, **kwargs)
            except exception as e:
                message1 = message if message is not None else '{}'.format(e)
                return JsonResponse({'error': message1}, status=status)
        return wrapped_view
    return decorator


@method_decorator(_handle_error(DeisClientError, status=500), 'dispatch')
@method_decorator(_handle_error(DeisClientTimeoutError, status=500, message='PaaS server timeout'), 'dispatch')
@method_decorator(_handle_deis_client_response_error, 'dispatch')
class ApiBaseView(View):
    deis_client = DeisClient(settings.DEIS_URL)

    def respond_multiple(self, items):
        """Returns a HTTP response for multiple items.

        @type items: list
            Must be a json-serializable list

        @rtype: django.http.HttpResponse
        """
        return JsonResponse({'results': items})

    def respond(self, item=None, status=None):
        """Returns a HTTP response. If ``item`` is None,
        then the HTTP status will be 204. Otherwise,
        the HTTP status will be ``status``, defaulting
        to 200.

        @type item: dict
            Must be json-serializable

        @rtype: django.http.HttpResponse
        """
        if item is None:
            return HttpResponse(status=204)
        else:
            status = 200 if status is None else status
            return JsonResponse(item, status=status)
