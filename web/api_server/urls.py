from django.conf.urls import url

from api_server import views
from api_server.api.addons_api_view import AddonsApiView
from api_server.api.addon_details_api_view import AddonDetailsApiView
from api_server.api.apps_api_view import AppsApiView
from api_server.api.app_collaborators_api_view import AppCollaboratorsApiView
from api_server.api.app_collaborator_details_api_view import AppCollaboratorDetailsApiView
from api_server.api.app_details_api_view import AppDetailsApiView
from api_server.api.app_domains_api_view import AppDomainsApiView
from api_server.api.app_domain_details_api_view import AppDomainDetailsApiView
from api_server.api.app_env_variables_api_view import AppEnvVariablesApiView
from api_server.api.app_log_api_view import AppLogApiView
from api_server.api.keys_api_view import KeysApiView
from api_server.api.key_details_api_view import KeyDetailsApiView
from api_server.api.paas_backends_api_view import PaasBackendApiView
from api_server.api.run_command_api_view import RunCommandApiView


urlpatterns = [
    url(r'^api_key/$', views.api_key_view, name='api_key'),
    url(r'^test_api_key/$', views.test_api_key, name='test_api_key'),
    url(r'^v1/apps/$', AppsApiView.as_view(), name='apps'),
    url(r'^v1/apps/([a-z0-9-]+)/$',
        AppDetailsApiView.as_view(), name='app_details'),
    url(r'^v1/apps/([a-z0-9-]+)/addons/$',
        AddonsApiView.as_view(), name='addons'),
    url(r'^v1/apps/([a-z0-9-]+)/addons/([a-zA-Z0-9-]+)/$',
        AddonDetailsApiView.as_view(), name='addon_details'),
    url(r'^v1/apps/([a-z0-9-]+)/collaborators/$',
        AppCollaboratorsApiView.as_view(), name='app_collaborators'),
    url(r'^v1/apps/([a-z0-9-]+)/collaborators/([a-z0-9]+)/$',
        AppCollaboratorDetailsApiView.as_view(), name='app_collaborator_details'),
    url(r'^v1/apps/([a-z0-9-]+)/domains/$',
        AppDomainsApiView.as_view(), name='app_domains'),
    url(r'^v1/apps/([a-z0-9-]+)/domains/([a-z0-9-_.]+)/$',
        AppDomainDetailsApiView.as_view(), name='app_domain_details'),
    url(r'^v1/apps/([a-z0-9-]+)/env/$',
        AppEnvVariablesApiView.as_view(), name='app_env_variables'),
    url(r'^v1/apps/([a-z0-9-]+)/log/$',
        AppLogApiView.as_view(), name='app_log'),
    url(r'^v1/apps/([a-z0-9-]+)/run/$',
        RunCommandApiView.as_view(), name='run_command'),
    url(r'^v1/keys/$', KeysApiView.as_view(), name='keys'),
    url(r'^v1/keys/([A-Za-z0-9_-]+)/([A-Za-z0-9_-]+)/$',
        KeyDetailsApiView.as_view(), name='key_details'),
    url(r'^v1/backends/$', PaasBackendApiView.as_view(), name='backends')
]
