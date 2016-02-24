from django.conf.urls import url, include
from django.contrib import admin

import cas.views


admin.autodiscover()

urlpatterns = [
    url(r'^api/', include('api_server.urls')),
    url(r'^login$', cas.views.login, name='cas_login'),
    url(r'^logout$', cas.views.login, name='cas_logout'),
]
