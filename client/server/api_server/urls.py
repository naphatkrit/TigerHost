from django.conf.urls import url

from api_server import views


urlpatterns = [
    url(r'^api_key/$', views.api_key_view, name='api_key')
]
