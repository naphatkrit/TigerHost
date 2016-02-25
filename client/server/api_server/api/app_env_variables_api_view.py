import json

from django.utils.decorators import method_decorator

from api_server.api.api_base_view import ApiBaseView
from wsse.decorators import check_wsse_token


@method_decorator(check_wsse_token, 'dispatch')
class AppEnvVariablesApiView(ApiBaseView):

    def get(self, request, app_id):
        """Get the environmental variables

        @type request: django.http.HttpRequest
        @type app_id: str

        @rtype: django.http.HttpResponse
        """
        auth_client, _ = self.deis_client.login_or_register(
            request.user.username, request.user.profile.get_paas_password(), request.user.email)

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

        @type request: django.http.HttpRequest
        @type app_id: str

        @rtype: django.http.HttpResponse
        """
        env_vars = json.loads(request.body)
        auth_client, _ = self.deis_client.login_or_register(
            request.user.username, request.user.profile.get_paas_password(), request.user.email)

        auth_client.set_application_env_variables(app_id, env_vars)
        return self.respond()
