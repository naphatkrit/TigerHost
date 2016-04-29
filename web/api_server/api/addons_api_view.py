import json
import re

from django.utils.decorators import method_decorator

from api_server.addons.providers.utils import get_provider_from_provider_name
from api_server.addons.state import AddonState, visible_states
from api_server.addons.state_machine_manager import StateMachineManager
from api_server.api.api_base_view import ApiBaseView, ErrorResponse
from api_server.models import Addon, App
from wsse.decorators import check_wsse_token


_valid_chars = r'[0-9a-zA-Z_]'

_value_regexp = re.compile(r'^{}*$'.format(_valid_chars))


@method_decorator(check_wsse_token, 'dispatch')
class AddonsApiView(ApiBaseView):

    def get(self, request, app_id):
        """Return all the addons installed for this application.

        :param django.http.HttpRequest request: the request object
        :param str app_id: the ID of the app

        :rtype: django.http.HttpResponse
        """
        addons = Addon.objects.filter(
            app__app_id=app_id, state__in=visible_states)
        items = [x.to_dict() for x in addons.all()]
        return self.respond_multiple(items)

    def post(self, request, app_id):
        """Add a new addon for this application.

        The body of the request should be a JSON with the following format:
        {
            'provider_name': 'provider_name',
            'config_customization': 'optional, either a string or None'
        }

        Returns a JSON with the following format:
        {
            'message': 'message to be displayed to user',
            'addon': {
                (the addon object)
            }
        }

        :param django.http.HttpRequest request: the request object

        :rtype: django.http.HttpResponse
        """
        app = App.objects.get(app_id=app_id)  # make sure app exists first
        data = json.loads(request.body)
        provider_name = data['provider_name']
        provider = get_provider_from_provider_name(provider_name)

        config_customization = data.get('config_customization', None)
        if config_customization is not None and not _value_regexp.match(config_customization):
            raise ErrorResponse(message='The customization string {} is invalid. Valid characters are {}.'.format(config_customization, _valid_chars), status=400)
        if config_customization is not None:
            config_customization = config_customization.upper()

        result = provider.begin_provision(app_id)
        addon = Addon.objects.create(
            provider_name=provider_name,
            provider_uuid=result['uuid'],
            app=app,
            state=AddonState.waiting_for_provision,
            user=request.user,
            config_customization=config_customization,
        )
        manager = StateMachineManager()
        manager.start_task(addon.id)
        return self.respond({'message': result['message'], 'addon': addon.to_dict()})
