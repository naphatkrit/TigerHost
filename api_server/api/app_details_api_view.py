import json

from django.utils.decorators import method_decorator

from api_server.api.api_base_view import ApiBaseView
from api_server.models import App
from api_server.providers import get_provider_authenticated_client, get_provider_api_url
from api_server.utils import git_remote
from wsse.decorators import check_wsse_token


@method_decorator(check_wsse_token, 'dispatch')
class AppDetailsApiView(ApiBaseView):

    def get(self, request, app_id):
        """Get information about this app.

        Returns a JSON with the following fields:
        {
            "owner": "userid",
            "remote": "ssh://git@hostname.com/app.git"
        }

        @type request: django.http.HttpRequest
        @type app_id: str

        @rtype: django.http.HttpResponse
        """
        provider = self.get_provider_for_app(app_id)
        auth_client = get_provider_authenticated_client(request.user.username, provider)

        owner = auth_client.get_application_owner(app_id)
        return self.respond({
            'owner': owner,
            'remote': git_remote(get_provider_api_url(provider), app_id)
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
        provider = self.get_provider_for_app(app_id)
        auth_client = get_provider_authenticated_client(request.user.username, provider)

        if 'owner' in data:
            self.ensure_user_exists(data['owner'], provider)
            auth_client.set_application_owner(app_id, data['owner'])
        return self.respond()

    def delete(self, request, app_id):
        """Delete an application

        @type request: django.http.HttpRequest
        @type app_id: str

        @rtype: django.http.HttpResponse
        """
        provider = self.get_provider_for_app(app_id)
        auth_client = get_provider_authenticated_client(request.user.username, provider)
        auth_client.delete_application(app_id)
        app = App.objects.get(app_id=app_id)
        app.delete()
        return self.respond()
