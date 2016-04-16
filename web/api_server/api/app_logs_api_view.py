from django.utils.decorators import method_decorator

from api_server.api.api_base_view import ApiBaseView
from api_server.paas_backends import get_backend_authenticated_client
from wsse.decorators import check_wsse_token


@method_decorator(check_wsse_token, 'dispatch')
class AppLogsApiView(ApiBaseView):

    def get(self, request, app_id):
        """Get the logs for this application

        Returns a JSON list of log entries (dict). Each entry has the following structure:{

            'process': 'run.1',

            'message': 'sample message',

            'app': 'sample-python',

            'timestamp': '2016-04-16T14:26:03UTC',

        }


        :param django.http.HttpRequest request: the request object
        :param str app_id: the ID of the app

        :rtype: django.http.HttpResponse
        """
        backend = self.get_backend_for_app(app_id)
        auth_client = get_backend_authenticated_client(
            request.user.username, backend)

        lines = request.GET.get('lines', None)
        if lines is not None:
            lines = int(lines)

        logs = auth_client.get_application_logs(app_id, lines)
        return self.respond_multiple(logs)
