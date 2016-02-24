from django.conf import settings
from django.http import JsonResponse
from django.views.generic import View

from api_server.clients.deis_client import DeisClient


class ApiBaseView(View):
    deis_client = DeisClient(settings.DEIS_URL)

    def respond_multiple(self, items):
        """Returns a HTTP response for multiple items.

        @type items: list
            Must be a json-serializable list

        @rtype: django.http.HttpResponse
        """
        return JsonResponse({'results': items})
