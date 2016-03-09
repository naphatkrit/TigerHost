import json

from django.utils.decorators import method_decorator

from api_server.addons.providers.utils import get_provider_from_provider_name
from api_server.addons.state import AddonState
from api_server.addons.state_machine_manager import StateMachineManager
from api_server.api.api_base_view import ApiBaseView
from api_server.models import Addon, App
from wsse.decorators import check_wsse_token


@method_decorator(check_wsse_token, 'dispatch')
class AddonsApiView(ApiBaseView):

    def get(self, request, app_id):
        """Return all the addons installed for this application.

        @type request: django.http.HttpRequest
        @type app_id: str

        @rtype: django.http.HttpResponse
        """
        # TODO must filter based on status as well
        addons = Addon.objects.filter(app__app_id=app_id)
        items = [{
            'name': x.display_name,
            'addon': x.provider_name,
        } for x in addons.all()]
        return self.respond_multiple(items)

    def post(self, request, app_id):
        """Add a new addon for this application.

        The body of the request should be a JSON with the following format:
        {
            'addon': 'addon',
        }

        Returns a JSON with the following format:
        {
            'message': 'message to be displayed to user',
            'name': 'the-name-of-the-addon-created'
        }

        @type request: django.http.HttpRequest

        @rtype: django.http.HttpResponse
        """
        app = App.objects.get(app_id=app_id)  # make sure app exists first
        data = json.loads(request.body)
        provider_name = data['addon']
        provider = get_provider_from_provider_name(provider_name)

        result = provider.begin_provision(app_id)
        addon = Addon.objects.create(
            provider_name=provider_name,
            provider_uuid=result['uuid'],
            app=app,
            state=AddonState.waiting_for_provision,
            user=request.user,
        )
        manager = StateMachineManager()
        manager.start_task(addon.id)
        return self.respond({'message': result['message'], 'name': addon.display_name})
