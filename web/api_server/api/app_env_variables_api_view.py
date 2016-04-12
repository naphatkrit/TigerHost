import json

from django.utils.decorators import method_decorator

from api_server.api.api_base_view import ApiBaseView
from api_server.paas_backends import get_backend_authenticated_client
from wsse.decorators import check_wsse_token


@method_decorator(check_wsse_token, 'dispatch')
class AppEnvVariablesApiView(ApiBaseView):

    def get(self, request, app_id):
        """Get the environmental variables

        :param django.http.HttpRequest request: the request object
        :param str app_id: the ID of the app

        :rtype: django.http.HttpResponse
        """
        backend = self.get_backend_for_app(app_id)
        auth_client = get_backend_authenticated_client(
            request.user.username, backend)

        env_vars = auth_client.get_application_env_variables(app_id)
        return self.respond(env_vars)

    def post(self, request, app_id):
        """Set the environmental variables

        The body of the request must be a JSON with the format
        {
            "VAR1": "value",
            "VAR2": "value2",
            ...
        }
        To unset a variable, set its value to ``null``.

        :param django.http.HttpRequest request: the request object
        :param str app_id: the ID of the app

        :rtype: django.http.HttpResponse
        """
        env_vars = json.loads(request.body)

        backend = self.get_backend_for_app(app_id)
        auth_client = get_backend_authenticated_client(
            request.user.username, backend)

        auth_client.set_application_env_variables(app_id, env_vars)
        return self.respond()
