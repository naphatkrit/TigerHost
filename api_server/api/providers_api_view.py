from django.conf import settings
from django.utils.decorators import method_decorator

from api_server.api.api_base_view import ApiBaseView
from wsse.decorators import check_wsse_token


@method_decorator(check_wsse_token, 'dispatch')
class ProvidersApiView(ApiBaseView):

    def get(self, request):
        """Get the list of providers that this user has access to.

        Return format (JSON):
        {
            'providers': ['provider1', 'provider2', ...]
            'default': 'provider1'
        }

        @type request: django.http.HttpRequest

        @rtype: django.http.HttpResponse
        """

        return self.respond({
            'providers': request.user.profile.get_providers(),
            'default': settings.DEFAULT_PAAS_PROVIDER,
        })
