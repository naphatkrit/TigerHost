from django.conf.urls import url

from api_server import views
from api_server.api.apps_api_view import AppsApiView


urlpatterns = [
    url(r'^api_key/$', views.api_key_view, name='api_key'),
    url(r'^v1/apps/$', AppsApiView.as_view(), name='apps'),
]
