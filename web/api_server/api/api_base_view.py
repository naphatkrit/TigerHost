from functools import wraps

from django.http import JsonResponse, HttpResponse
from django.utils.decorators import available_attrs, method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from api_server.addons.providers.exceptions import AddonProviderError
from api_server.addons.state_machine_manager import StateMachineError
from api_server.clients.exceptions import ClientResponseError, ClientError, ClientTimeoutError
from api_server.models import App
from api_server.paas_backends import get_backend_authenticated_client, BackendsError, BackendsUserError


def _handle_deis_client_response_error(f):
    @wraps(f, assigned=available_attrs(f))
    def wrapped_view(request, *args, **kwargs):
        try:
            return f(request, *args, **kwargs)
        except ClientResponseError as e:
            try:
                return JsonResponse(e.response.json(), status=e.response.status_code)
            except ValueError:
                return HttpResponse(e.response.text, status=e.response.status_code)
    return wrapped_view


def _handle_error(exception, status, message=None):
    """A decorator that gracefully handles errors, instead of 500'ing
    """
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


class ErrorResponse(Exception):
    """Raise this to easily return an error to the cilent.
    """
    def __init__(self, message, status):
        super(ErrorResponse, self).__init__(message)
        self.status = status


def _handle_error_response(f):
    @wraps(f, assigned=available_attrs(f))
    def wrapped_view(request, *args, **kwargs):
        try:
            return f(request, *args, **kwargs)
        except ErrorResponse as e:
            return JsonResponse({'error': '{}'.format(e)}, status=e.status)
    return wrapped_view


@method_decorator(csrf_exempt, 'dispatch')
@method_decorator(_handle_error(Exception, status=500), 'dispatch')
@method_decorator(_handle_error(ClientError, status=500), 'dispatch')
@method_decorator(_handle_error(ClientTimeoutError, status=500, message='PaaS server timeout'), 'dispatch')
@method_decorator(_handle_error(BackendsError, status=500), 'dispatch')
@method_decorator(_handle_error(BackendsUserError, status=400), 'dispatch')
@method_decorator(_handle_error(StateMachineError, status=500), 'dispatch')
@method_decorator(_handle_error(AddonProviderError, status=500), 'dispatch')
@method_decorator(_handle_deis_client_response_error, 'dispatch')
@method_decorator(_handle_error_response, 'dispatch')
class ApiBaseView(View):

    def respond_multiple(self, items):
        """Returns a HTTP response for multiple items.

        :param list items: a json-serializable list

        :rtype: django.http.HttpResponse
        """
        return JsonResponse({'results': items})

    def respond(self, item=None, status=None):
        """Returns a HTTP response. If ``item`` is None,
        then the HTTP status will be 204. Otherwise,
        the HTTP status will be ``status``, defaulting
        to 200.

        :param dict item: a json-serializable dict

        :rtype: django.http.HttpResponse
        """
        if item is None:
            return HttpResponse(status=204)
        else:
            status = 200 if status is None else status
            return JsonResponse(item, status=status)

    def ensure_user_exists(self, username, backend):
        """Ensure the user with :code:`username` exists, both locally
        and on the specified backend. If the user does not exist locally,
        returns False. If the user does not exist on the backend, create it,
        but return True.

        :param str username: the username to ensure
        :param str backend: the PaaS backend to ensure on

        :raises api_server.clients.exceptions.ClientError:
        :raises api_server.paas_backends.BackendsError:
        """
        get_backend_authenticated_client(username, backend)

    def get_backend_for_app(self, app_id):
        """Returns the backend for this app, throwing
        an exception with an appropriate error message
        if the app does not exist.

        :param str app_id: the app ID

        :rtype: str
        :returns: the backend

        :raises api_server.api.api_base_view.ErrorResponse:
        """
        try:
            return App.objects.get(app_id=app_id).backend
        except App.DoesNotExist:
            raise ErrorResponse(
                message='App {} does not exist.'.format(app_id), status=400)
