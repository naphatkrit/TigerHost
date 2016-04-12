from django.conf import settings
from django.utils.decorators import method_decorator

from api_server.api.api_base_view import ApiBaseView
from wsse.decorators import check_wsse_token


@method_decorator(check_wsse_token, 'dispatch')
class PaasBackendApiView(ApiBaseView):

    def get(self, request):
        """Get the list of backends that this user has access to.

        Return format (JSON):
        {
            'backends': ['backend1', 'backend2', ...]
            'default': 'backend1'
        }

        :param django.http.HttpRequest request: the request object

        :rtype: django.http.HttpResponse
        """

        return self.respond({
            'backends': request.user.profile.get_paas_backends(),
            'default': settings.DEFAULT_PAAS_BACKEND,
        })
