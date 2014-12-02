# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('importcsv.inputs',
    url(r'^list/$', 'list', name='list'),
)
