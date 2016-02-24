from functools import wraps

from django.conf import settings
from django.http import JsonResponse
from django.utils.decorators import available_attrs, method_decorator
from django.views.generic import View

from api_server.clients.deis_client_errors import DeisClientResponseError
from api_server.clients.deis_client import DeisClient


def _handle_deis_client_response_error(f):
    @wraps(f, assigned=available_attrs(f))
    def wrapped_view(request, *args, **kwargs):
        try:
            return f(request, *args, **kwargs)
        except DeisClientResponseError as e:
            return JsonResponse(e.response.json(), status=e.response.status_code)
    return wrapped_view


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
