
 #-*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404, render, render_to_response
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from django.forms.models import model_to_dict
from django.db.models import Q
from navigation.models import *
from navigation.currency import *

		
def log_in(request, next='/'):
	logout(request)
	username = password = ''
	if request.POST:
		username = request.POST.get('username', 'none')
		password = request.POST.get('password', 'none')
		next = request.POST.get('next', 'none')
		next = next[next.index('//')+2:]
		next = next[next.index('/'):]
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
	return HttpResponseRedirect(next)
	
def log_out(request):
	logout(request)
	return HttpResponseRedirect('/')
	  
def listPersonnes(request):

	if request.POST: #Pour le trie par ordre alphabétique et la pagination
		startwith = request.POST.get('start_with', '')
		page = int(request.POST.get('page_num', '1'))
	else :
		startwith = ''
		page = 1
		
	personnes = Personne.objects.all().filter(Q(nom__startswith=startwith) | Q(prenom__startswith=startwith)).order_by('nom','prenom')  
	page_nb = len(personnes)/20 + 1
	personnes = personnes[20*(page-1):20*page]
  
	personnes_nom = [(personne.id, personne.titre_personne+" "+personne.nom+" "+personne.prenom) for personne in personnes]
					    
	return render_to_response('page_list.html',
		{'title':'Personnes', 'active':'personnes', 'list':personnes_nom, 'link':'/personnes/', 
		'page_nb': page_nb, 'start_with': startwith, 'page_num': page },
		context_instance=RequestContext(request))

def listPieces(request):

	if request.POST: #Pour le trie par ordre alphabétique et la pagination
		startwith = request.POST.get('start_with', '')
		page = int(request.POST.get('page_num', '1'))
	else :
		startwith = ''
		page = 1

	pieces = Piece.objects.all().filter(titre__startswith=startwith).order_by('titre')  
	page_nb = len(pieces)/20 + 1
	pieces = pieces[20*(page-1):20*page]

	piece_titre = [(piece.id, piece.titre) for piece in pieces]

	return render_to_response('page_list.html',
	{'title':'Pieces', 'active':'pieces', 'list':piece_titre, 'link':'/pieces/', 
	'page_nb': page_nb, 'start_with': startwith, 'page_num': page },
	context_instance=RequestContext(request))
      
def listSoirees(request,date='1700-01-01'):

 	soirees = Soiree.objects.all()
	soireesVide = SoireeVide.objects.all()
	soiree_date = []

	for soiree in soirees:
		soiree_date.append({'date' : str(soiree.date), 'value' : 'filled'})
	for soireeVide in soireesVide:
		soiree_date.append({'date' : str(soireeVide.date), 'value' : 'empty'})
	
	return render_to_response('page_list_soiree.html',
	{'title':'Accueil', 'active':'accueil', 'data':soiree_date, 'date':date, 'link':'/soirees/'},
	context_instance=RequestContext(request))
	
def detailsPersonne(request,id):
  personne=Personne.objects.get(id=id)
  personne_nationalite=personne.get_nationalite_display()
  personne_genre=personne.get_genre_display()
  return render_to_response('page_detail_personne.html',
    {'title':personne.prenom+' '+personne.nom,
    'active':'personnes',
    'personneinfos':personne,
    'personne_nationalite':personne_nationalite,
    'personne_genre':personne_genre},
    context_instance=RequestContext(request))

def detailsPiece(request,id):
  piece=Piece.objects.get(id=id)
  piece_langue=piece.get_langue_display()
  return render_to_response('page_detail_piece.html',
    {'title':piece.titre,
    'active':'pieces',
    'pieceinfos':piece,
    'piece_langue':piece_langue,},
    context_instance=RequestContext(request))

def detailsSoiree(request,date):
	try :
		soiree = Soiree.objects.get(date = date)
		billetteries = Billetterie.objects.all().filter(budget = soiree.budget)
		debits = Debit.objects.all().filter(budget = soiree.budget)			
		credits = Credit.objects.all().filter(budget = soiree.budget).exclude(id__in=billetteries)
		liste_representations = []
		representations = Representation.objects.all().filter(Soiree = soiree)
		animations = Animation.objects.all().filter(Soiree = soiree)
		for rep in representations : 
			liste_representations.append(rep)
		for rep in animations : 
			liste_representations.append(rep)
	except ObjectDoesNotExist as e:
		try :
			soiree = SoireeVide.objects.get(date = date)
		except ObjectDoesNotExist as e:
			return listSoirees(request,date)
		return render_to_response('page_detail_soiree.html',
	    {'title':str(soiree.date),
	    'active':'soirees',
	    'soireeinfos':soiree},
	    context_instance=RequestContext(request))
	return render_to_response('page_detail_soiree.html',
    {'title':str(soiree.date),
    'active':'soirees',
    'soireeinfos':soiree,
		'billetterieinfos':billetteries,
		'debitsinfos':debits,
		'creditsinfos':credits,
		'liste_representations': liste_representations},
    context_instance=RequestContext(request))

