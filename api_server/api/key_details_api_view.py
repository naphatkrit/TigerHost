from django.utils.decorators import method_decorator

from api_server.api.api_base_view import ApiBaseView
from wsse.decorators import check_wsse_token


@method_decorator(check_wsse_token, 'dispatch')
class KeyDetailsApiView(ApiBaseView):

    def delete(self, request, key_name):
        """Remove a key from the user

        @type request: django.http.HttpRequest
        @type key_name: str

        @rtype: django.http.HttpResponse
        """
        auth_client, _ = self.deis_client.login_or_register(
            request.user.username, request.user.profile.get_paas_password(), request.user.email)

        auth_client.remove_key(key_name)
        return self.respond()
