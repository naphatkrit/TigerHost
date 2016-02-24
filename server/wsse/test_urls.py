from django.conf.urls import url

from wsse import views


urlpatterns = [
    url(r'^wsse_test/$', views.test_view, name='wsse_test'),
    url(r'^wsse_class_test/$', views.TestView.as_view(), name='wsse_class_test'),
]
