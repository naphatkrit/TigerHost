from functools import wraps

from django.http import JsonResponse, HttpResponse
from django.utils.decorators import available_attrs, method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from api_server.clients.deis_client_errors import DeisClientResponseError, DeisClientError, DeisClientTimeoutError
from api_server.models import App
from api_server.providers import get_provider_authenticated_client, ProvidersError, ProvidersUserError


def _handle_deis_client_response_error(f):
    @wraps(f, assigned=available_attrs(f))
    def wrapped_view(request, *args, **kwargs):
        try:
            return f(request, *args, **kwargs)
        except DeisClientResponseError as e:
            try:
                return JsonResponse(e.response.json(), status=e.response.status_code)
            except ValueError:
                return HttpResponse(e.response.text, status=e.response.status_code)
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


@method_decorator(csrf_exempt, 'dispatch')
@method_decorator(_handle_error(Exception, status=500), 'dispatch')
@method_decorator(_handle_error(DeisClientError, status=500), 'dispatch')
@method_decorator(_handle_error(DeisClientTimeoutError, status=500, message='PaaS server timeout'), 'dispatch')
@method_decorator(_handle_error(ProvidersError, status=500), 'dispatch')
@method_decorator(_handle_error(ProvidersUserError, status=400), 'dispatch')
@method_decorator(_handle_error(App.DoesNotExist, status=400, message="App does not exist."), 'dispatch')
@method_decorator(_handle_deis_client_response_error, 'dispatch')
class ApiBaseView(View):

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

    def respond_error(self, message, status):
        """Returns a HTTP response to indicate an error.

        @type message: str
        @type status: int

        @rtype django.http.HttpResponse
        """
        return JsonResponse({
            'error': message
        }, status=status)

    def ensure_user_exists(self, username, provider):
        """Ensure the user with ``username`` exists, both locally
        and on Deis. If the user does not exist locally, returns
        False. If the user does not exist on Deis,
        create it, but return True.

        @type username: str
        @type provider: str

        @raises e: DeisClientError
        @raises e: ProvidersError
        """
        get_provider_authenticated_client(username, provider)
