from django.utils.decorators import method_decorator

from api_server.api.api_base_view import ApiBaseView
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
        auth_client, _ = self.deis_client.login_or_register(
            request.user.username, request.user.profile.get_paas_password(), request.user.email)

        auth_client.remove_application_collaborator(app_id, username)
        return self.respond()
