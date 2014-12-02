from django.conf.urls import patterns, url
from stats import views

urlpatterns = patterns('',
  # .../saisie/
  url(r'^$', views.statsForm),   
	)
