from django.utils.decorators import method_decorator

from api_server.api.api_base_view import ApiBaseView
from api_server.paas_backends import get_backend_authenticated_client
from wsse.decorators import check_wsse_token


@method_decorator(check_wsse_token, 'dispatch')
class KeyDetailsApiView(ApiBaseView):

    def delete(self, request, backend, key_name):
        """Remove a key from the user

        @type request: django.http.HttpRequest

        :param django.http.HttpRequest request: the request object
        :param str backend: the PaaS backend to add this key to
        :param str key_name: the name of the key

        :rtype: django.http.HttpResponse
        """
        auth_client = get_backend_authenticated_client(
            request.user.username, backend)

        auth_client.remove_key(key_name)
        return self.respond()
