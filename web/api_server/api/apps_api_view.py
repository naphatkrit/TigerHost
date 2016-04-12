import json

from django.conf import settings
from django.db import IntegrityError
from django.utils.decorators import method_decorator

from api_server.api.api_base_view import ApiBaseView, ErrorResponse
from api_server.models import App
from api_server.paas_backends import get_backend_authenticated_client
from wsse.decorators import check_wsse_token


@method_decorator(check_wsse_token, 'dispatch')
class AppsApiView(ApiBaseView):

    def get(self, request):
        """Return the list of applications associated with this user.

        Return format (JSON):
        {
            'backend1': ['app1', ...],
            'backend2': ['app1', ...],
            ...
        }

        :param django.http.HttpRequest request: the request object

        :rtype: django.http.HttpResponse
        """
        result = {}
        for backend in request.user.profile.get_paas_backends():
            auth_client = get_backend_authenticated_client(
                request.user.username, backend)
            result[backend] = auth_client.get_all_applications()
        return self.respond(result)

    def post(self, request):
        """Create a new application.

        The body of the request should be a JSON with the following format:
        {
            'id': 'app_id_here',
            'backend': 'backend',
        }
        If the 'backend' field is not provided, then the default is used.

        :param django.http.HttpRequest request: the request object

        :rtype: django.http.HttpResponse
        """
        data = json.loads(request.body)
        app_id = data['id']
        backend = data.get('backend', settings.DEFAULT_PAAS_BACKEND)

        # is the user authorized to use this backend?
        auth_client = get_backend_authenticated_client(
            request.user.username, backend)

        # is there already an app with this ID?
        try:
            app = App.objects.create(app_id=app_id, backend=backend)
        except IntegrityError:
            raise ErrorResponse('App {} already exists. Please pick a new name.'.format(app_id), status=400)

        try:
            auth_client.create_application(app_id)
        except Exception:
            # on any kind of errors, must delete the app object,
            # as we essentially took a lock on the name when we
            # created the object
            app.delete()

            # reraise the exception
            raise

        return self.respond()
