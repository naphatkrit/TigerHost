import json

from django.utils.decorators import method_decorator

from api_server.api.api_base_view import ApiBaseView
from api_server.providers import get_provider_authenticated_client
from wsse.decorators import check_wsse_token


@method_decorator(check_wsse_token, 'dispatch')
class AppDomainsApiView(ApiBaseView):

    def get(self, request, app_id):
        """Get the domains associated with this app

        @type request: django.http.HttpRequest
        @type app_id: str

        @rtype: django.http.HttpResponse
        """
        provider = self.get_provider_for_app(app_id)
        auth_client = get_provider_authenticated_client(
            request.user.username, provider)

        domains = auth_client.get_application_domains(app_id)
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
        provider = self.get_provider_for_app(app_id)
        auth_client = get_provider_authenticated_client(
            request.user.username, provider)

        auth_client.add_application_domain(app_id, domain)
        return self.respond()
