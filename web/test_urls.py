from urls import urlpatterns
from django.conf.urls import url, include

urlpatterns += [
    url(r'^', include('wsse.test_urls'))
]
