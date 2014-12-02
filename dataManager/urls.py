from django.conf.urls import patterns, url

from dataManager import views

urlpatterns = patterns('',
    # ex: /saisie/
    url(r'^$', views.index, name='index'),
    # ex: /saisie/5/
    url(r'^(?P<saisie_id>\d+)/$', views.detail, name='detail'),
    # ex: /saisie/5/results/
    url(r'^(?P<saisie_id>\d+)/results/$', views.results, name='results'),
    # ex: /saisie/5/vote/
    url(r'^(?P<saisie_id>\d+)/vote/$', views.vote, name='vote'),
	# ex: /dataManager/importation/file.yml
	url(r'^importation/$', views.importation, name='importation'),	
	url(r'^test/$', views.test, name='importation'),
)