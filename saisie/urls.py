from django.conf.urls import patterns, url
from saisie import views, cesar, theaville

urlpatterns = patterns('',
  # .../saisie/
  url(r'^$', views.saisie),  
  url(r'^info/personne/(?P<nom>\w+)/(?P<prenom>\w*)$', cesar.searchPersonne),
  url(r'^info/piece/(?P<titre>\w+)$', theaville.searchPiece),
  url(r'^info/personne/(?P<id>\d+)$', cesar.getInfoPersonne),
	url(r'^info/piece/(?P<id>\d+)$', theaville.getInfoPiece),
	url(r'^new/personne/$', views.creerPersonne),
  url(r'^new/piece/$', views.creerPiece),
  url(r'^new/soiree/$', views.creerSoiree),
	url(r'^new/soireeVide/(?P<date>\d{4}-\d{2}-\d{2})$', views.creerSoireeVide),
	url(r'^soiree/(?P<date>\d{4}-\d{2}-\d{2})$', views.saisie),
	url(r'^update/(?P<type>\w+)/(?P<id>\d+)$', views.update),
	url(r'^delete/(?P<type>\w+)/(?P<id>\d+)$', views.delete),
	)
