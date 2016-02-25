from django.conf.urls import url

from api_server import views
from api_server.api.apps_api_view import AppsApiView
from api_server.api.app_details_api_view import AppDetailsApiView
from api_server.api.app_domains_api_view import AppDomainsApiView
from api_server.api.app_domain_details_api_view import AppDomainDetailsApiView
from api_server.api.app_env_variables_api_view import AppEnvVariablesApiView


urlpatterns = [
    url(r'^api_key/$', views.api_key_view, name='api_key'),
    url(r'^v1/apps/$', AppsApiView.as_view(), name='apps'),
    url(r'^v1/apps/([a-z0-9]+)/$', AppDetailsApiView.as_view(), name='app_details'),
    url(r'^v1/apps/([a-z0-9]+)/domains/$', AppDomainsApiView.as_view(), name='app_domains'),
    url(r'^v1/apps/([a-z0-9]+)/domains/([a-z0-9.]+)/$', AppDomainDetailsApiView.as_view(), name='app_domain_details'),
    url(r'^v1/apps/([a-z0-9]+)/env/$', AppEnvVariablesApiView.as_view(), name='app_env_variables'),
]
