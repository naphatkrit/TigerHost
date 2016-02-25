import json

from django.utils.decorators import method_decorator

from api_server.api.api_base_view import ApiBaseView
from wsse.decorators import check_wsse_token


@method_decorator(check_wsse_token, 'dispatch')
class AppDetailsApiView(ApiBaseView):

    def get(self, request, app_id):
        """Get information about this app.

        Returns a JSON with the following fields:
        {
            "owner": "userid"
        }

        @type request: django.http.HttpRequest
        @type app_id: str

        @rtype: django.http.HttpResponse
        """
        auth_client, _ = self.deis_client.login_or_register(
            request.user.username, request.user.profile.get_paas_password(), request.user.email)

        owner = auth_client.get_application_owner(app_id)
        return self.respond({
            'owner': owner
        })

    def post(self, request, app_id):
        """Update information about this app.

        The request body must be a JSON with any subset of the following fields:
        {
            "owner": "userid"
        }

        @type request: django.http.HttpRequest
        @type app_id: str

        @rtype: django.http.HttpResponse
        """
        data = json.loads(request.body)
        auth_client, _ = self.deis_client.login_or_register(
            request.user.username, request.user.profile.get_paas_password(), request.user.email)

        if 'owner' in data:
            auth_client.set_application_owner(app_id, data['owner'])
        return self.respond()

    def delete(self, request, app_id):
        """Delete an application

        @type request: django.http.HttpRequest
        @type app_id: str

        @rtype: django.http.HttpResponse
        """
        auth_client, _ = self.deis_client.login_or_register(
            request.user.username, request.user.profile.get_paas_password(), request.user.email)

        auth_client.delete_application(app_id)
        return self.respond()
