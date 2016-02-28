from django.utils.decorators import method_decorator

from api_server.api.api_base_view import ApiBaseView
from wsse.decorators import check_wsse_token


@method_decorator(check_wsse_token, 'dispatch')
class AppDomainDetailsApiView(ApiBaseView):

    def delete(self, request, app_id, domain):
        """Remove a domain from the app

        @type request: django.http.HttpRequest
        @type app_id: str
        @type domain: str

        @rtype: django.http.HttpResponse
        """
        auth_client, _ = self.deis_client.login_or_register(
            request.user.username, request.user.profile.get_paas_password(), request.user.email)

        auth_client.remove_application_domain(app_id, domain)
        return self.respond()
