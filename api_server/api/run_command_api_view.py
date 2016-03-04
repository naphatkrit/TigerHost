import json

from django.utils.decorators import method_decorator

from api_server.api.api_base_view import ApiBaseView
from api_server.providers import get_provider_authenticated_client
from wsse.decorators import check_wsse_token


@method_decorator(check_wsse_token, 'dispatch')
class RunCommandApiView(ApiBaseView):

    def post(self, request, app_id):
        """Run a one-off command.

        The request body must be a JSON with the following fields:
        {
            "command": "echo 1 2 3"
        }

        @type request: django.http.HttpRequest
        @type app_id: str

        @rtype: django.http.HttpResponse
        """
        command = json.loads(request.body)['command']
        provider = self.get_provider_for_app(app_id)
        auth_client = get_provider_authenticated_client(
            request.user.username, provider)

        return self.respond(auth_client.run_command(app_id, command))
