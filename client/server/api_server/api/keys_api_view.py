import json

from django.utils.decorators import method_decorator

from api_server.api.api_base_view import ApiBaseView
from wsse.decorators import check_wsse_token


@method_decorator(check_wsse_token, 'dispatch')
class KeysApiView(ApiBaseView):

    def get(self, request):
        """Get the list of public keys for this user.

        @type request: django.http.HttpRequest

        @rtype: django.http.HttpResponse
        """
        auth_client, _ = self.deis_client.login_or_register(
            request.user.username, request.user.profile.get_paas_password(), request.user.email)

        info = auth_client.get_keys()
        return self.respond_multiple(info)

    def post(self, request):
        """Add a key to the list of keys for this user.

        The body of the request must be a JSON with the format
        {
            "key_name": "macbookpro",
            "key": "ssh-rsa ..."
        }

        @type request: django.http.HttpRequest

        @rtype: django.http.HttpResponse
        """
        key_info = json.loads(request.body)
        auth_client, _ = self.deis_client.login_or_register(
            request.user.username, request.user.profile.get_paas_password(), request.user.email)

        auth_client.add_key(key_info['key_name'], key_info['key'])
        return self.respond()
