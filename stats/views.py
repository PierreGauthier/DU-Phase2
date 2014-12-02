 #-*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from django.template import RequestContext
from navigation.models import *
from datetime import timedelta
import datetime

	
def statsForm(request):
	results = ""
	prev_criteria = []
	list = {}
	if request.POST:
	
		soirees = Soiree.objects.all().filter(date__gte=request.POST['datestatfrom'], date__lte=request.POST['datestatto'])
		personnes = []
		pieces = []
		prev_criteria.append(('datestatfrom',request.POST['datestatfrom']))
		prev_criteria.append(('datestatto',request.POST['datestatto']))		
		prev_criteria.append(('dateby',request.POST['dateby']))	
		prev_criteria.append(('infoOn',request.POST['infoOn']))
		
		isPersonneDefined = False		
		isPieceDefined = False			
		
		lastNbConcerne = int(request.POST['lastConcerneIndex']) 
		nbConcerne = 0
		for i in range(0,lastNbConcerne+1):			
			relation = request.POST.get('concerne'+str(i)+'relation','none')
			type = request.POST.get('concerne'+str(i)+'type','none')
			element = request.POST.get('concerne'+str(i)+'element','none')
			if relation != 'none' :
				if relation == 'avec':
					if type == 'personne':
						isPersonneDefined = True
						if element != u'0':
							personnes.append(Personne.objects.get(id=element))
						else :
							personnes += Personne.objects.all()
					if type == 'piece':
						isPieceDefined = True
						if element != u'0':
							pieces.append(Piece.objects.get(id=element))
						else :
							pieces += Piece.objects.all()
				prev_criteria.append(('concerne'+str(nbConcerne)+'relation',relation))	
				prev_criteria.append(('concerne'+str(nbConcerne)+'type',type))	
				prev_criteria.append(('concerne'+str(nbConcerne)+'element',element))
				nbConcerne += 1	
		
		if not isPersonneDefined : personnes = [ p for p in Personne.objects.all() ]
		if not isPieceDefined : pieces = [ p for p in Piece.objects.all() ]
		
		list['soirees'] = { str(x.date):str(x) for x in soirees }
		list['personnes'] = { x.id:str(x) for x in personnes }
		list['pieces'] = { x.id:str(x) for x in pieces }
		
		results += render_to_string('page_stat_piece.html' , 
		{'data':statsPiece(8),"list": list, },
		context_instance=RequestContext(request))
		
	return render_to_response('page_stats.html', {
		"title":"Rechercher", "active":"rechercher", 
		"all_personnes":[ (x.id,x.nom + ' ' + x.prenom) for x in Personne.objects.all().order_by('nom') ],
		"all_pieces":[ (x.id,x.titre) for x in Piece.objects.all().order_by('titre') ], 
		"results":results, "previous_criteria":prev_criteria}, 
		context_instance=RequestContext(request))	
	

		
def quantize(data,freq,func):
	dates = data.keys()	
	newData = {}	
	
	if freq == 'semaine':
		for date in daterange(min(dates),max(dates),'week'):
			newData[date] = 0
		for k,v in data.items():
			if func == 'sum' : newData[datetime.date(k.year,k.month,k.day/7*7+1)] += data[k]
			else : newData[datetime.date(k.year,k.month,k.day/7*7+1)] += 1
			
	elif freq == 'mois':
		for date in daterange(min(dates),max(dates),'month'):
			newData[date] = 0
		for k,v in data.items():
			if func == 'sum' : newData[datetime.date(k.year,k.month,1)] += data[k]
			else : newData[datetime.date(k.year,k.month,1)] += 1
			
	elif freq == 'ans':
		for date in daterange(min(dates),max(dates),'year'):
			newData[date] = 0
		for k,v in data.items():
			if func == 'sum' : newData[datetime.date(k.year,1,1)] += data[k]
			else : newData[datetime.date(k.year,1,1)] += 1
			
	elif freq == 'decennie':
		for date in daterange(min(dates),max(dates),'decade'):
			newData[date] = 0
		for k,v in data.items():
			if func == 'sum' : newData[datetime.date(k.year/10*10,1,1)] += data[k]
			else : newData[datetime.date(k.year/10*10,1,1)] += 1
	else :
		for date in daterange(min(dates),max(dates),'day'):
			newData[date] = 0
		for k,v in data.items():
			if func == 'sum' : newData[datetime.date(k.year,k.month,k.day)] += data[k]
			else : newData[datetime.date(k.year,k.month,k.day)] += 1
			
	return newData
		
		
def daterange(start, end, delta):
	if delta == 'day':
		curr = start
		offset = timedelta(days=1)
		while curr < end:
			yield curr
			curr += offset
	elif delta == 'week':
		curr = datetime.date(start.year, start.month, 1)
		offset = timedelta(weeks=1)
		while curr < end:
			yield curr
			curr += offset
	elif delta == 'month':
		curr = datetime.date(start.year, start.month, 1)
		while curr < end:
			if curr.month == 12:
				new = datetime.date(curr.year+1, 1, curr.day)
			else:
				new = datetime.date(curr.year, curr.month+1, curr.day)
			yield curr
			curr = new
	elif delta == 'year':
		curr = datetime.date(start.year, 1, 1)
		while curr < end:
			new = datetime.date(curr.year+1, curr.month, curr.day)
			yield curr
			curr = new
	elif delta == 'decade':
		curr = datetime.date(start.year/10*10, 1, 1)
		while curr < end:
			new = datetime.date(curr.year+10, curr.month, curr.day)
			yield curr
			curr = new
		
def statsPiece(id,f='1700-01-01',t='1799-12-31'):

	piece = Piece.objects.get(id=id)
	soireesPeriode = Soiree.objects.all().filter(date__gte=f, date__lte=t)
	representations = Representation.objects.all().filter(piece=piece, Soiree__in=soireesPeriode)
	soirees = [x.Soiree for x in representations]

	statPiece = {}
	statPiece2 = {}
	
	statPiece['name'] = piece.titre
	statPiece['moyNbSpec'] = sum([x.budget.nb_total_billets_vendus_reg for x in soirees])/len(soirees)
	statPiece['nbRep'] = len(representations)
	statPiece['nbSpecMeta'] = {'x' : 'date', 'y' : 'nbSpectateur', 'opt' : {'langue': ['fr','it'], 'position' : ['1','2']}}
	statPiece['nbSpecLMeta'] = {'x' : 'date', 'y' : ['nbSpectateur','nbSpecPremiereLoge','nbSpecParterre']}
	statPiece2['nbSpec'] = [ {'date': str(x.Soiree.date), 
														'nbSpectateur': x.Soiree.budget.nb_total_billets_vendus_reg,
														'langue': str(x.piece.langue),
														'position': x.position } for x in representations]
	statPiece['pie'] = {
		'Jouée Avec' : [
			{'rep' : 'nbJoueAvec', 'color' : 'nomPiece'},
			] + [ 
			{'nbJoueAvec': 7, 'nomPiece' : 'Alceste'},
			{'nbJoueAvec': 2, 'nomPiece' : 'truc'},
			{'nbJoueAvec': 1, 'nomPiece' : 'test'},
			{'nbJoueAvec': 3, 'nomPiece' : 'blabla'},
			{'nbJoueAvec': 2, 'nomPiece' : 'machin'},
			{'nbJoueAvec': 7, 'nomPiece' : 'Alceste2'},
			{'nbJoueAvec': 2, 'nomPiece' : 'truc2'},
			{'nbJoueAvec': 1, 'nomPiece' : 'test2'},
			{'nbJoueAvec': 3, 'nomPiece' : 'blabla2'}
		],
		'Musicien' : [
			{'rep' : 'nbJoue', 'color' : 'avecsans'},
			{'nbJoue': 10, 'avecsans' : 'Avec'},
			{'nbJoue': 5, 'avecsans' : 'Sans'},
		]}
	
	statPiece2['name'] = 'Stat Piece'	
	statPiece2['moyNbSpec'] = 123
	statPiece2['nbRep'] = 25
	statPiece['nbSpec'] = [	
		{'date': '1700-01-05', 'nbSpectateur' : 124, 'langue' : 'fr', 'position' : '1'},
		{'date': '1700-02-09', 'nbSpectateur' : 334, 'langue' : 'fr', 'position' : '1'},
		{'date': '1700-03-05', 'nbSpectateur' : 129, 'langue' : 'it', 'position' : '1'},
		{'date': '1700-03-12', 'nbSpectateur' : 126, 'langue' : 'fr', 'position' : '2'},
		{'date': '1700-07-05', 'nbSpectateur' : 134, 'langue' : 'fr', 'position' : '1'},
		{'date': '1700-09-10', 'nbSpectateur' : 234, 'langue' : 'it', 'position' : '2'},
		{'date': '1700-09-05', 'nbSpectateur' : 224, 'langue' : 'fr', 'position' : '2'},
		{'date': '1700-10-20', 'nbSpectateur' : 103, 'langue' : 'fr', 'position' : '2'},
		{'date': '1700-02-05', 'nbSpectateur' : 634, 'langue' : 'it', 'position' : '2'},
		{'date': '1700-03-23', 'nbSpectateur' : 414, 'langue' : 'fr', 'position' : '2'},
		{'date': '1700-04-05', 'nbSpectateur' : 234, 'langue' : 'fr', 'position' : '2'},
		{'date': '1700-06-05', 'nbSpectateur' : 934, 'langue' : 'it', 'position' : '1'},
		{'date': '1700-02-28', 'nbSpectateur' : 94, 'langue' : 'it', 'position' : '2'},
		{'date': '1700-08-05', 'nbSpectateur' : 34, 'langue' : 'fr', 'position' : '1'},
		{'date': '1700-09-05', 'nbSpectateur' : 224, 'langue' : 'it', 'position' : '1'},
		{'date': '1700-10-30', 'nbSpectateur' : 144, 'langue' : 'it', 'position' : '1'},
		{'date': '1700-11-05', 'nbSpectateur' : 234, 'langue' : 'fr', 'position' : '1'},
		{'date': '1700-12-31', 'nbSpectateur' : 324, 'langue' : 'fr', 'position' : '2'}
	]
	statPiece['nbSpecL'] = [	
		{'date': '1700-01-01', 'nbSpectateur' : 1024, 'nbSpecPremiereLoge' : 453, 'nbSpecParterre' : 732},
		{'date': '1700-01-02', 'nbSpectateur' : 1234, 'nbSpecPremiereLoge' : 423, 'nbSpecParterre' : 756},
		{'date': '1700-01-03', 'nbSpectateur' : 124, 'nbSpecPremiereLoge' : 253, 'nbSpecParterre' : 742},
		{'date': '1700-01-04', 'nbSpectateur' : 2124, 'nbSpecPremiereLoge' : 53, 'nbSpecParterre' : 832},
		{'date': '1700-01-05', 'nbSpectateur' : 3124, 'nbSpecPremiereLoge' : 453, 'nbSpecParterre' : 752},
		{'date': '1700-01-06', 'nbSpectateur' : 1240, 'nbSpecPremiereLoge' : 353, 'nbSpecParterre' : 733},
		{'date': '1700-01-07', 'nbSpectateur' : 124, 'nbSpecPremiereLoge' : 423, 'nbSpecParterre' : 732},
		{'date': '1700-01-08', 'nbSpectateur' : 924, 'nbSpecPremiereLoge' : 413, 'nbSpecParterre' : 732},
		{'date': '1700-01-09', 'nbSpectateur' : 3521, 'nbSpecPremiereLoge' : 153, 'nbSpecParterre' : 12},
		{'date': '1700-01-10', 'nbSpectateur' : 1524, 'nbSpecPremiereLoge' : 423, 'nbSpecParterre' : 732},
		{'date': '1700-01-11', 'nbSpectateur' : 6124, 'nbSpecPremiereLoge' : 413, 'nbSpecParterre' : 732},
		{'date': '1700-01-12', 'nbSpectateur' : 7124, 'nbSpecPremiereLoge' : 153, 'nbSpecParterre' : 732},
		{'date': '1700-01-13', 'nbSpectateur' : 4124, 'nbSpecPremiereLoge' : 423, 'nbSpecParterre' : 932},
		{'date': '1700-01-14', 'nbSpectateur' : 3124, 'nbSpecPremiereLoge' : 353, 'nbSpecParterre' : 732},
		{'date': '1700-01-15', 'nbSpectateur' : 1124, 'nbSpecPremiereLoge' : 753, 'nbSpecParterre' : 432},
		{'date': '1700-01-16', 'nbSpectateur' : 524, 'nbSpecPremiereLoge' : 253, 'nbSpecParterre' : 132},
		{'date': '1700-01-17', 'nbSpectateur' : 1254, 'nbSpecPremiereLoge' : 273, 'nbSpecParterre' : 732},
		{'date': '1700-01-18', 'nbSpectateur' : 5124, 'nbSpecPremiereLoge' : 363, 'nbSpecParterre' : 632},
		{'date': '1700-01-19', 'nbSpectateur' : 4224, 'nbSpecPremiereLoge' : 513, 'nbSpecParterre' : 732},
		{'date': '1700-01-20', 'nbSpectateur' : 224, 'nbSpecPremiereLoge' : 823, 'nbSpecParterre' : 762},
		{'date': '1700-01-21', 'nbSpectateur' : 1224, 'nbSpecPremiereLoge' : 903, 'nbSpecParterre' : 632}
	]
	statPiece2['pie'] = {
		'Jouée Avec' : [
			{'rep' : 'nbJoueAvec', 'color' : 'nomPiece'},
			{'nbJoueAvec': 7, 'nomPiece' : 'Alceste'},
			{'nbJoueAvec': 2, 'nomPiece' : 'truc'},
			{'nbJoueAvec': 1, 'nomPiece' : 'test'},
			{'nbJoueAvec': 3, 'nomPiece' : 'blabla'},
			{'nbJoueAvec': 2, 'nomPiece' : 'machin'},
			{'nbJoueAvec': 7, 'nomPiece' : 'Alceste2'},
			{'nbJoueAvec': 2, 'nomPiece' : 'truc2'},
			{'nbJoueAvec': 1, 'nomPiece' : 'test2'},
			{'nbJoueAvec': 3, 'nomPiece' : 'blabla2'}
		],
		'Musicien' : [
			{'rep' : 'nbJoue', 'color' : 'avecsans'},
			{'nbJoue': 10, 'avecsans' : 'Avec'},
			{'nbJoue': 5, 'avecsans' : 'Sans'},
		]}
	statPiece2['complet'] = 78

	return statPiece