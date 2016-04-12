import json

from django.utils.decorators import method_decorator

from api_server.api.api_base_view import ApiBaseView
from api_server.paas_backends import get_backend_authenticated_client
from wsse.decorators import check_wsse_token


@method_decorator(check_wsse_token, 'dispatch')
class AppCollaboratorsApiView(ApiBaseView):

    def get(self, request, app_id):
        """Get the list of usernames who are collaborators on
        this app. This does NOT include the app owner.

        :param django.http.HttpRequest request: the request object
        :param str app_id: the ID of the app

        :rtype: django.http.HttpResponse
        """
        backend = self.get_backend_for_app(app_id)
        auth_client = get_backend_authenticated_client(
            request.user.username, backend)

        users = auth_client.get_application_collaborators(app_id)
        return self.respond_multiple(users)

    def post(self, request, app_id):
        """Add a collaborator to this app.

        The body of the request must be a JSON with the format
        {
            "username": "userid",
        }

        :param django.http.HttpRequest request: the request object
        :param str app_id: the ID of the app

        :rtype: django.http.HttpResponse
        """
        username = json.loads(request.body)['username']

        backend = self.get_backend_for_app(app_id)
        auth_client = get_backend_authenticated_client(
            request.user.username, backend)

        self.ensure_user_exists(username, backend)

        auth_client.add_application_collaborator(app_id, username)
        return self.respond()
