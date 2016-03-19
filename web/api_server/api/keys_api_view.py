import json

from django.utils.decorators import method_decorator

from api_server.api.api_base_view import ApiBaseView
from api_server.paas_backends import get_backend_authenticated_client
from wsse.decorators import check_wsse_token


@method_decorator(check_wsse_token, 'dispatch')
class KeysApiView(ApiBaseView):

    def get(self, request):
        """Get the list of public keys for this user.

        Return format (JSON):
        {
            'backend1': [{
                            "key_name": "my_key_name",
                            "key": "ssh-rsa ..."
                            }, ...],
            'backend2': [...],
            ...
        }

        @type request: django.http.HttpRequest

        @rtype: django.http.HttpResponse
        """
        result = {}
        for backend in request.user.profile.get_paas_backends():
            auth_client = get_backend_authenticated_client(
                request.user.username, backend)
            result[backend] = auth_client.get_keys()
        return self.respond(result)

    def post(self, request):
        """Add a key to the list of keys for this user.

        The body of the request must be a JSON with the format
        {
            "key_name": "macbookpro",
            "key": "ssh-rsa ...",
            "backend": "backend"
        }

        @type request: django.http.HttpRequest

        @rtype: django.http.HttpResponse
        """
        key_info = json.loads(request.body)

        backend = key_info['backend']
        auth_client = get_backend_authenticated_client(
            request.user.username, backend)

        auth_client.add_key(key_info['key_name'], key_info['key'])
        return self.respond()
