from django.utils.decorators import method_decorator

from api_server.addons.event import AddonEvent
from api_server.addons.providers.utils import get_provider_from_provider_name
from api_server.addons.state import visible_states
from api_server.addons.state_machine_manager import StateMachineManager
from api_server.api.api_base_view import ApiBaseView
from api_server.models import Addon
from wsse.decorators import check_wsse_token


@method_decorator(check_wsse_token, 'dispatch')
class AddonDetailsApiView(ApiBaseView):

    def get(self, request, app_id, addon_name):
        """Return all the addons installed for this application.

        :param django.http.HttpRequest request: the request object
        :param str app_id: the ID of the app

        :rtype: django.http.HttpResponse
        """
        addon = Addon.objects.get(app__app_id=app_id, display_name=addon_name, state__in=visible_states)
        return self.respond(addon.to_dict())

    def delete(self, request, app_id, addon_name):
        """Return all the addons installed for this application.

        :param django.http.HttpRequest request: the request object
        :param str app_id: the ID of the app

        :rtype: django.http.HttpResponse
        """
        addon = Addon.objects.get(app__app_id=app_id, display_name=addon_name)
        provider = get_provider_from_provider_name(addon.provider_name)
        result = provider.deprovision(addon.provider_uuid)
        manager = StateMachineManager()
        with manager.transition(addon.id, AddonEvent.deprovision_success):
            pass
        manager.start_task(addon.id)
        return self.respond({'message': result['message']})
