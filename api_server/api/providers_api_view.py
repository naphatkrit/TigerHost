from django.utils.decorators import method_decorator

from api_server.api.api_base_view import ApiBaseView
from wsse.decorators import check_wsse_token


@method_decorator(check_wsse_token, 'dispatch')
class ProvidersApiView(ApiBaseView):

    def get(self, request):
        """Get the list of providers that this user has access to.

        @type request: django.http.HttpRequest

        @rtype: django.http.HttpResponse
        """
        return self.respond_multiple(request.user.profile.get_providers())
