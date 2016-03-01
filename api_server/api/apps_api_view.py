import json

from django.conf import settings
from django.db import IntegrityError
from django.utils.decorators import method_decorator

from api_server.api.api_base_view import ApiBaseView
from api_server.models import App
from api_server.providers import get_provider_authenticated_client
from wsse.decorators import check_wsse_token


@method_decorator(check_wsse_token, 'dispatch')
class AppsApiView(ApiBaseView):

    def get(self, request):
        """Return the list of applications associated with this user.

        @type request: django.http.HttpRequest

        @rtype: django.http.HttpResponse
        """
        app_ids = []
        for provider in request.user.profile.get_providers():
            auth_client = get_provider_authenticated_client(
                request.user.username, provider)
            app_ids += auth_client.get_all_applications()
        return self.respond_multiple(app_ids)

    def post(self, request):
        """Create a new application.

        The body of the request should be a JSON with the following format:
        {
            'id': 'app_id_here',
            'provider': 'provider_name',
        }
        If the 'provider' field is not provided, then the default is used.

        @type request: django.http.HttpRequest

        @rtype: django.http.HttpResponse
        """
        data = json.loads(request.body)
        app_id = data['id']
        provider = data.get('provider', settings.DEFAULT_PAAS_PROVIDER)

        # is the user authorized to use this provider?
        auth_client = get_provider_authenticated_client(
            request.user.username, provider)

        # is there already an app with this ID?
        try:
            app = App.objects.create(app_id=app_id, provider_name=provider)
        except IntegrityError:
            return self.respond_error(message='App {} already exists. Please pick a new name.'.format(app), status=400)

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
