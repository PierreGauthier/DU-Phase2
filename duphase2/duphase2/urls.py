from django.conf.urls import patterns, include, url
from django.contrib import admin

from presphase2 import views

urlpatterns = patterns('',
    # Examples:
    url(r'^$', views.home),
    url(r'^admin/', include(admin.site.urls)),
)
