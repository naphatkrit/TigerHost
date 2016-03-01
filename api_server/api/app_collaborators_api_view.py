import json

from django.utils.decorators import method_decorator

from api_server.api.api_base_view import ApiBaseView
from api_server.providers import get_provider_authenticated_client
from wsse.decorators import check_wsse_token


@method_decorator(check_wsse_token, 'dispatch')
class AppCollaboratorsApiView(ApiBaseView):

    def get(self, request, app_id):
        """Get the list of usernames who are collaborators on
        this app. This does NOT include the app owner.

        @type request: django.http.HttpRequest
        @type app_id: str

        @rtype: django.http.HttpResponse
        """
        provider = self.get_provider_for_app(app_id)
        auth_client = get_provider_authenticated_client(
            request.user.username, provider)

        users = auth_client.get_application_collaborators(app_id)
        return self.respond_multiple(users)

    def post(self, request, app_id):
        """Add a collaborator to this app.

        The body of the request must be a JSON with the format
        {
            "username": "userid",
        }

        @type request: django.http.HttpRequest
        @type app_id: str

        @rtype: django.http.HttpResponse
        """
        username = json.loads(request.body)['username']

        provider = self.get_provider_for_app(app_id)
        auth_client = get_provider_authenticated_client(
            request.user.username, provider)

        self.ensure_user_exists(username, provider)

        auth_client.add_application_collaborator(app_id, username)
        return self.respond()
