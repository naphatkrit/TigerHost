import json

from django.utils.decorators import method_decorator

from api_server.api.api_base_view import ApiBaseView
from api_server.paas_backends import get_backend_authenticated_client
from wsse.decorators import check_wsse_token


@method_decorator(check_wsse_token, 'dispatch')
class RunCommandApiView(ApiBaseView):

    def post(self, request, app_id):
        """Run a one-off command.

        The request body must be a JSON with the following fields:
        {
            "command": "echo 1 2 3"
        }

        :param django.http.HttpRequest request: the request object
        :param str app_id: the ID of the app

        :rtype: django.http.HttpResponse
        """
        command = json.loads(request.body)['command']
        backend = self.get_backend_for_app(app_id)
        auth_client = get_backend_authenticated_client(
            request.user.username, backend)

        return self.respond(auth_client.run_command(app_id, command))
