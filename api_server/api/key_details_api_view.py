from django.conf import settings
from django.utils.decorators import method_decorator

from api_server.api.api_base_view import ApiBaseView
from api_server.providers import get_provider_authenticated_client
from wsse.decorators import check_wsse_token


@method_decorator(check_wsse_token, 'dispatch')
class KeyDetailsApiView(ApiBaseView):

    def delete(self, request, key_name):
        """Remove a key from the user

        @type request: django.http.HttpRequest
        @type key_name: str

        @rtype: django.http.HttpResponse
        """
        # TODO figure out how this plays with providers

        provider = settings.DEFAULT_PAAS_PROVIDER
        auth_client = get_provider_authenticated_client(
            request.user.username, provider)

        auth_client.remove_key(key_name)
        return self.respond()
