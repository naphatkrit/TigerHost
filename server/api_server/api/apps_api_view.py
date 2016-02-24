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
