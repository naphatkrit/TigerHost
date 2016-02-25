import json

from django.utils.decorators import method_decorator

from api_server.api.api_base_view import ApiBaseView
from wsse.decorators import check_wsse_token


@method_decorator(check_wsse_token, 'dispatch')
class AppDomainsApiView(ApiBaseView):

    def get(self, request, app_id):
        """Get the domains associated with this app

        @type request: django.http.HttpRequest
        @type app_id: str

        @rtype: django.http.HttpResponse
        """
        auth_client, _ = self.deis_client.login_or_register(
            request.user.username, request.user.profile.get_paas_password(), request.user.email)

        domains = auth_client.get_application_domains()
        return self.respond_multiple(domains)

    def post(self, request, app_id):
        """Add a domain to this app

        The body of the request must be a JSON with the format
        {
            "domain": "example.com",
        }

        @type request: django.http.HttpRequest
        @type app_id: str

        @rtype: django.http.HttpResponse
        """
        domain = json.loads(request.body)['domain']
        auth_client, _ = self.deis_client.login_or_register(
            request.user.username, request.user.profile.get_paas_password(), request.user.email)

        auth_client.add_application_domain(app_id, domain)
        return self.respond()
