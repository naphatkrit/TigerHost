import json

from django.utils.decorators import method_decorator

from api_server.api.api_base_view import ApiBaseView
from wsse.decorators import check_wsse_token


@method_decorator(check_wsse_token, 'dispatch')
class AppsApiView(ApiBaseView):

    def get(self, request):
        """Return the list of applications associated with this user.

        @type request: django.http.HttpRequest

        @rtype: django.http.HttpResponse
        """
        auth_client, _ = self.deis_client.login_or_register(
            request.user.username, request.user.profile.get_paas_password(), request.user.email)

        app_ids = auth_client.get_all_applications()
        return self.respond_multiple(app_ids)

    def post(self, request):
        """Create a new application.

        The body of the request should be a JSON with the following format:
        {
            'id': 'app_id_here'
        }

        @type request: django.http.HttpRequest

        @rtype: django.http.HttpResponse
        """
        app_id = json.loads(request.body)['id']
        auth_client, _ = self.deis_client.login_or_register(
            request.user.username, request.user.profile.get_paas_password(), request.user.email)

        auth_client.create_application(app_id)
        return self.respond()
