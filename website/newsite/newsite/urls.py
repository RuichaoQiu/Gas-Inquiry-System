from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^gm/', include('gm.urls', namespace="gm")),
    url(r'^admin/', include(admin.site.urls)),
)