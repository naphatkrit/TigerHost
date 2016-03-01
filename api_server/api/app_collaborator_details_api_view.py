from django.utils.decorators import method_decorator

from api_server.api.api_base_view import ApiBaseView
from api_server.providers import get_provider_authenticated_client
from wsse.decorators import check_wsse_token


@method_decorator(check_wsse_token, 'dispatch')
class AppCollaboratorDetailsApiView(ApiBaseView):

    def delete(self, request, app_id, username):
        """Remove a collaborator from the app

        @type request: django.http.HttpRequest
        @type app_id: str
        @type domain: str
        @type username

        @rtype: django.http.HttpResponse
        """
        provider = self.get_provider_for_app(app_id)
        auth_client = get_provider_authenticated_client(
            request.user.username, provider)

        auth_client.remove_application_collaborator(app_id, username)
        return self.respond()
