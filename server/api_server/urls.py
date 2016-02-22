from django.conf.urls import url

from api_server import views


urlpatterns = [
    url(r'^token/$', views.token_generate_page, name='token_generation')
]
