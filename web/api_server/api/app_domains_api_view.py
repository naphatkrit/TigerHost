import json

from django.utils.decorators import method_decorator

from api_server.api.api_base_view import ApiBaseView
from api_server.paas_backends import get_backend_authenticated_client
from wsse.decorators import check_wsse_token


@method_decorator(check_wsse_token, 'dispatch')
class AppDomainsApiView(ApiBaseView):

    def get(self, request, app_id):
        """Get the domains associated with this app

        :param django.http.HttpRequest request: the request object
        :param str app_id: the ID of the app

        :rtype: django.http.HttpResponse
        """
        backend = self.get_backend_for_app(app_id)
        auth_client = get_backend_authenticated_client(
            request.user.username, backend)

        domains = auth_client.get_application_domains(app_id)
        return self.respond_multiple(domains)

    def post(self, request, app_id):
        """Add a domain to this app

        The body of the request must be a JSON with the format
        {
            "domain": "example.com",
        }

        :param django.http.HttpRequest request: the request object
        :param str app_id: the ID of the app

        :rtype: django.http.HttpResponse
        """
        domain = json.loads(request.body)['domain']
        backend = self.get_backend_for_app(app_id)
        auth_client = get_backend_authenticated_client(
            request.user.username, backend)

        auth_client.add_application_domain(app_id, domain)
        return self.respond()
