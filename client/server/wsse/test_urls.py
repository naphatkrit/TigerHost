from django.conf.urls import url

from wsse import views


urlpatterns = [
    url(r'^wsse_test/$', views.test_view, name='wsse_test')
]
