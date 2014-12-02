 #-*- coding: utf-8 -*-
 
from django.shortcuts import get_object_or_404, render, render_to_response
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from django.forms.models import model_to_dict
from django.db import IntegrityError
from navigation.models import *
from navigation.currency import *
from saisie.forms import *
import re, ast

	
@login_required(login_url='/login/')
def saisie(request, active_tab='Soiree', alert='off', alert_type='success', alert_message="unknown", previous_values = {}, date=''):

	# Quand on click sur une case vide du calendrier
	if date != '' :
		previous_values['soireeForm'] = {} 
		previous_values['soireeForm']['date'] = date

	personneForm = render_to_string(
		'form.html' , 
		{'action' : '/saisie/new/personne/', 'formset_list' : {'PersonneForm':PersonneForm()},
		'date_picker_id_list' : ['dpersonne1','dpersonne2'], 'previous_values' : previous_values, 
		'specific_function' : 'saisie_personne.js', 'alertZoneId':'azpersonne', 'formId':'personneForm'},
		context_instance=RequestContext(request)) + render_to_string(
		'modal.html' , 
		{'modalId' : 'personneModal', 'modalTitle' : 'Recherche sur Cesar', 'modalFoot' : True},
		context_instance=RequestContext(request))

	pieceForm = render_to_string(
		'form.html' , 
		{'action' : '/saisie/new/piece/', 'formset_list' : {'PieceForm':PieceForm()}, 
		'date_picker_id_list' : ['dpiece1'],b'previous_values' : previous_values, 
		'specific_function' : 'saisie_piece.js', 'alertZoneId':'azpiece', 'formId':'pieceForm'},
		context_instance=RequestContext(request)) + render_to_string(
		'modal.html' , 
		{'modalId' : 'pieceModal', 'modalTitle' : 'Recherche sur Theaville', 'modalFoot' : True},
		context_instance=RequestContext(request))

	soireeForm = render_to_string(
		'form_soiree.html' , 
		{'action' : '/saisie/new/soiree/', 
		'formset_list' : { 'PageRegistreForm' : PageRegistreForm(), 'SoireeForm' : SoireeForm(), 'BudgetSoireeForm' : BudgetSoireeForm()}, 
		'formitems' : {'representation': RepresentationForm, 'animation': AnimationForm() ,'debit':DebitForm(),
		'credit':CreditForm(),'billetterie':BilletterieForm(), 'role':RoleForm()}, 'formId' : 'soireeForm',
		'previous_values' : previous_values, 'specific_function' : 'saisie_soiree.js', 'date_picker_id_list' : ['dsoiree1']},
		context_instance=RequestContext(request))

	return render_to_response('page_tab.html', 
		{"title":"Saisie", "active":"saisie", "tab_list" : 
		{"Personne" : personneForm, "Soiree":soireeForm, "Piece":pieceForm}, "active_tab":active_tab, 
		'alert' : alert, 'alert_type' : alert_type, 'alert_message' : alert_message}, 
		context_instance=RequestContext(request))
				

@login_required(login_url='/login/')
def creerPersonne(request):
	if request.POST:		
		data = { x:y for x,y in request.POST.iteritems() }
		data = testDateForm(data,['date_de_naissance','date_de_deces'])	
		
		# Info concernant la piece ou la soirée depuis laquele la personne à été créée
		data['other_information'] = data['other_information'].replace('&', '","')
		data['other_information'] = data['other_information'].replace('=', '":"')		
		data['other_information'] = data['other_information'].replace('+', ' ')
		prevData = {}
		if data['other_information']=='':
			goBackTo = 'Personne'
		else :
			goBackTo = 'Soiree'
			prevData['soireeForm'] = ast.literal_eval('{"' + data['other_information'] + '"}')
		del data['other_information']
		
		# Si c'est un update plutot qu'un insert
		id = data['personneForm_id']
		del data['personneForm_id']
		if id != '': 	#update
			instance = Personne.objects.get(id=int(id))
			personne = PersonneForm(data, instance=instance)			
			message = data['prenom'] + ' ' + data['nom'] + u'</a></b> a bien été mise à jour'
		else :				#insert			
			personne = PersonneForm(data)			
			message = data['prenom'] + ' ' + data['nom'] + u'</a></b> a bien été ajouté dans la base'
			
			
		try:
			instance = personne.save()
			message = u'<b><a href="/personnes/' + str(instance.id) + '">' + message
			return saisie(request, active_tab=goBackTo,alert='on',alert_type='success',alert_message=message, previous_values = prevData)
		except ValidationError as e:
			message = ' '.join(e.messages)
			return saisie(request, active_tab='Personne',alert='on',alert_type='danger',alert_message=message, 
			  previous_values = request.POST)
		except ValueError as e:
			message = e
			return saisie(request, active_tab='Personne',alert='on',alert_type='danger',alert_message=message, 
			  previous_values = request.POST)
                      
@login_required(login_url='/login/')
def creerPiece(request):
	if request.POST:	
		data = { x:y for x,y in request.POST.iteritems() }
		data = testDateForm(data,['date_premiere'])	
		if 'auteurs' in data : del data['auteurs']
		
		# Info concernant la piece ou la soirée depuis laquele la personne à été créée
		data['other_information'] = data['other_information'].replace('&', '","')
		data['other_information'] = data['other_information'].replace('=', '":"')		
		data['other_information'] = data['other_information'].replace('+', ' ')
		prevData = {}
		if data['other_information']=='':
			goBackTo = 'Piece'
		else :
			goBackTo = 'Soiree'
			prevData['soireeForm'] = ast.literal_eval('{"' + data['other_information'] + '"}')
		del data['other_information']

		auteurs = [ Personne.objects.get(id=int(x)) for x in request.POST.getlist('auteurs')]
		
		# Si c'est un update plutot qu'un insert
		id = data['pieceForm_id']
		del data['pieceForm_id']
		if id != '': 	#update		
			instance = Piece.objects.get(id=int(id))
			piece = PieceForm(data, instance=instance)
			message = data['titre']  + u'</a></b> a bien été mise à jour'		
		else :				#insert
			piece = PieceForm(data)
			message = data['titre'] + u'</a></b> a bien été ajouté dans la base'
		
		try:
			instance = piece.save()
			message = u'<b><a href="/pieces/' + str(instance.id) + u'">' + message
			for auteur in auteurs : instance.auteurs.add(auteur)
			return saisie(request, active_tab='Piece',alert='on',alert_type='success',alert_message=message)
		except ValidationError as e:
			message = ' '.join(e.messages)
			return saisie(request, active_tab='Piece',alert='on',alert_type='danger',alert_message=message, 
				previous_values = request.POST)
		except ValueError as e:
			message = e
			return saisie(request, active_tab='Piece',alert='on',alert_type='danger',alert_message=message, 
			  previous_values = request.POST)
        

@login_required(login_url='/login/')
def creerSoiree(request):
	if request.POST:
	
		previous_values = {'soireeForm':request.POST}
		
		#Page Registre
		page_registre = PageRegistreForm(request.POST)
		try : page_registre.save()
		except ValueError as e:
			try :
				page_registre = PageRegistre.objects.get(ref_registre=request.POST['ref_registre'], num_page_pdf=request.POST['num_page_pdf'])
			except Exception as e:
				message = "Erreur concernant la page de registre (le numéro de page doit etre un nombre)"
				return saisie(request, active_tab='Soiree',alert='on',alert_type='danger',alert_message=message,
				  previous_values = previous_values)

		try :
			#budget soiree
			total_depenses_reg = currencyToNumber(request.POST.get('total_depenses_reg', 'none'))
			nb_total_billets_vendus_reg = request.POST.get('nb_total_billets_vendus_reg', 'none')
			total_recettes_reg = currencyToNumber(request.POST.get('total_recettes_reg', 'none'))
			debit_derniere_soiree_reg = currencyToNumber(request.POST.get('debit_derniere_soiree_reg', 'none'))
			total_depenses_corrige_reg = currencyToNumber(request.POST.get('total_depenses_corrige_reg', 'none'))
			quart_pauvre_reg = currencyToNumber(request.POST.get('quart_pauvre_reg', 'none'))
			debit_initial_reg = currencyToNumber(request.POST.get('debit_initial_reg', 'none'))
			reste_reg = currencyToNumber(request.POST.get('reste_reg', 'none'))
			nombre_cachets = request.POST.get('nombre_cachets', 'none').replace(',','.')
			montant_cachet = request.POST.get('montant_cachet', 'none')
			montant_cachet_auteur = currencyToNumber(request.POST.get('montant_cachet_auteur', 'none'))
			credit_final_reg = currencyToNumber(request.POST.get('credit_final_reg', 'none'))
			id = request.POST.get('budget_id', '')

			if id != '':
				budgetSoiree = BudgetSoiree(id=int(id), total_depenses_reg=total_depenses_reg, nb_total_billets_vendus_reg=nb_total_billets_vendus_reg, total_recettes_reg=total_recettes_reg, debit_derniere_soiree_reg=debit_derniere_soiree_reg, total_depenses_corrige_reg=total_depenses_corrige_reg, quart_pauvre_reg=quart_pauvre_reg, debit_initial_reg=debit_initial_reg, reste_reg=reste_reg, nombre_cachets=nombre_cachets, montant_cachet=montant_cachet, montant_cachet_auteur=montant_cachet_auteur, credit_final_reg=credit_final_reg) #update
			else : 				
				budgetSoiree = BudgetSoiree(total_depenses_reg=total_depenses_reg, nb_total_billets_vendus_reg=nb_total_billets_vendus_reg, total_recettes_reg=total_recettes_reg, debit_derniere_soiree_reg=debit_derniere_soiree_reg, total_depenses_corrige_reg=total_depenses_corrige_reg, quart_pauvre_reg=quart_pauvre_reg, debit_initial_reg=debit_initial_reg, reste_reg=reste_reg, nombre_cachets=nombre_cachets, montant_cachet=montant_cachet, montant_cachet_auteur=montant_cachet_auteur, credit_final_reg=credit_final_reg) #insert
			budgetSoiree.save()
			
			#debits
			list_debits = [ x.id for x in Debit.objects.all()]
			list_new_debits = []
			nb_debit = 0
			montant = request.POST.get('debit'+str(nb_debit)+'montant', 'none')
			while montant != 'none' :
				libelle = request.POST.get('debit'+str(nb_debit)+'libelle', 'none')
				type_depense = request.POST.get('debit'+str(nb_debit)+'type_depense', 'none')
				traduction = request.POST.get('debit'+str(nb_debit)+'traduction', 'none')
				mots_clefs = request.POST.get('debit'+str(nb_debit)+'mots_clefs', 'none')
				id = request.POST.get('debit'+str(nb_debit)+'id', '')
				nb_debit += 1
				if id == '' :
					debit = Debit(montant=currencyToNumber(montant), libelle=libelle, type_depense=type_depense, traduction=traduction, mots_clefs=mots_clefs, budget=budgetSoiree)
				else :
					debit = Debit(id=int(id), montant=currencyToNumber(montant), libelle=libelle, type_depense=type_depense, traduction=traduction, mots_clefs=mots_clefs, budget=budgetSoiree)
				debit.save()
				list_new_debits.append(debit.id)				
				montant = request.POST.get('debit'+str(nb_debit)+'montant', 'none')
					
			for el in list_debits :
				if el not in list_new_debits :
					Debit.objects.get(id=el).delete()
		
			#credits
			nb_credit = 0
			montant = request.POST.get('credit'+str(nb_credit)+'montant', 'none')
			while montant != 'none' :
				libelle = request.POST.get('credit'+str(nb_credit)+'libelle', 'none')
				id = request.POST.get('credit'+str(nb_debit)+'id', '')
				nb_credit += 1
				if id == '' :
					credit = Credit(montant=currencyToNumber(montant), libelle=libelle, budget=budgetSoiree)
				else :
					credit = Credit(id=int(id), montant=currencyToNumber(montant), libelle=libelle, budget=budgetSoiree)
				credit.save()
				montant = request.POST.get('credit'+str(nb_credit)+'montant', 'none')

			#billetteries
			nb_billetterie = 0
			montant = request.POST.get('billetterie'+str(nb_billetterie)+'montant', 'none')
			while montant != 'none' :
				libelle = request.POST.get('billetterie'+str(nb_billetterie)+'libelle_debit', 'none')
				nombre_billets_vendus = request.POST.get('billetterie'+str(nb_billetterie)+'nombre_billets_vendus', 'none')
				type_billet = request.POST.get('billetterie'+str(nb_billetterie)+'type_billet', 'none')
				commentaire = request.POST.get('billetterie'+str(nb_billetterie)+'commentaire', 'none')
				id = request.POST.get('billetterie'+str(nb_debit)+'id', 'none')
				nb_billetterie += 1
				if id == '' :
					billetterie = Billetterie(montant=currencyToNumber(montant), libelle=libelle, budget=budgetSoiree, nombre_billets_vendus=nombre_billets_vendus, type_billet=type_billet, commentaire=commentaire)
				else :
					billetterie = Billetterie(id=int(id), montant=currencyToNumber(montant), libelle=libelle, budget=budgetSoiree, nombre_billets_vendus=nombre_billets_vendus, type_billet=type_billet, commentaire=commentaire)
				billetterie.save()
				montant = request.POST.get('billetterie'+str(nb_billetterie)+'montant', 'none')

			#Soiree
			date = request.POST.get('date', 'none')
			libelle_date_reg = request.POST.get('libelle_date_reg', 'none')
			ligne_src = request.POST.get('ligne_src', 'none') 
			idSoiree = request.POST.get('soireeForm_id', '')
			if idSoiree == '':
				soiree = Soiree(date=date, libelle_date_reg=libelle_date_reg, budget=budgetSoiree, ligne_src=ligne_src, page_registre=page_registre)
			else :
				soiree = Soiree(id=int(idSoiree), date=date, libelle_date_reg=libelle_date_reg, budget=budgetSoiree, ligne_src=ligne_src, page_registre=page_registre)
			soiree.save()
			
			#representations
			nb_representations = 0
			position = request.POST.get('representation'+str(nb_representations)+'position', 'none')
			while position != 'none' :
				piece = request.POST.get('representation'+str(nb_representations)+'piece', 'none')
				id = request.POST.get('representation'+str(nb_representations)+'id', 'none')
				nb_representations += 1
				if id == '' : 
					representation = Representation(position=position, piece=Piece.objects.get(id=int(piece)), Soiree=soiree)
				else :
					representation = Representation(id=int(id), position=position, piece=Piece.objects.get(id=int(piece)), Soiree=soiree)
				representation.save()
				position = request.POST.get('representation'+str(nb_representations)+'position', 'none')
			
			#animations	
			nb_animations = 0
			position = request.POST.get('animation'+str(nb_animations)+'position', 'none')
			while position != 'none' :
				type = request.POST.get('animation'+str(nb_animations)+'type', 'none')
				auteur = request.POST.get('animation'+str(nb_animations)+'auteur', 'none')
				description = request.POST.get('animation'+str(nb_animations)+'description', 'none')
				id = request.POST.get('animation'+str(nb_debit)+'id', 'none')
				nb_animations += 1
				if id == '' : 
					animation = Animation(position=position, type=type, auteur=Personne.objects.get(id=int(auteur)), description=description, Soiree=soiree)
				else :
					animation = Animation(id=int(id), position=position, type=type, auteur=Personne.objects.get(id=int(auteur)), description=description, Soiree=soiree)
				animation.save()
				position = request.POST.get('animation'+str(nb_animations)+'position', 'none')
			
			#role
			nb_role = 0
			personne = request.POST.get('role'+str(nb_role)+'personne', 'none')
			while personne != 'none' :
				representation = request.POST.get('role'+str(nb_role)+'representation', 'none')
				roleField = request.POST.get('role'+str(nb_role)+'role', 'none')
				plus_dinfo = request.POST.get('role'+str(nb_role)+'plus_dinfo', 'none')
				id = request.POST.get('role'+str(nb_role)+'id', 'none')
				nb_role += 1
				if id == '' : 
					role = Role(personne=Personne.objects.get(id=int(personne)), representation=Representation.objects.get(Soiree=soiree, position=int(representation)), role=roleField, plus_dinfo=plus_dinfo)
				else :
					role = Role(id=int(id), personne=Personne.objects.get(id=int(personne)), representation=Representation.objects.get(Soiree=soiree, position=int(representation)), role=roleField, plus_dinfo=plus_dinfo)
				role.save()
				personne = request.POST.get('role'+str(nb_role)+'personne', 'none')
				
			if idSoiree == '' :
				message = u"La soirée du<a href='/soirees/"+soiree.date+"'><b> " + date + u"</b></a> a bien été ajouté dans la base"
			else :
				message = u"La soirée du<a href='/soirees/"+soiree.date+"'><b> " + date + u"</b></a> a bien été mise à jour"
			return saisie(request, active_tab='Soiree',alert='on',alert_type='success',alert_message=message)
		except ValidationError as e:
			message = ' '.join(e.messages)
			return saisie(request, active_tab='Soiree',alert='on',alert_type='danger',alert_message=message,
			  previous_values = previous_values)
		except IntegrityError:
			message = 'Une soiree utilise déjà cette page de registre'
			return saisie(request, active_tab='Soiree',alert='on',alert_type='danger',alert_message=message,
			  previous_values = previous_values)
		except CurrencyError as e:
			message = 'Une valeur monnétaire n\'a pas été entré correctement : livre,sou,denier'
			return saisie(request, active_tab='Soiree',alert='on',alert_type='danger',alert_message=message,
			  previous_values = previous_values)
		except Exception as e:
			message = str(e)
			return saisie(request, active_tab='Soiree',alert='on',alert_type='danger',alert_message=message,
			  previous_values = previous_values)
			

@login_required(login_url='/login/')
def creerSoireeVide(request, date):
	soiree = Soiree.objects.all().filter(date=date) # Vérification si la soirée n'a pas déjà été remplis
	if len(soiree) == 0 :
		soireevide = SoireeVide.objects.all().filter(date=date) # Vérification si la soirée n'a pas déjà été enregistrer comme vide
		if len(soireevide) == 0 :
			newSoireeVide = SoireeVide(date=date)
			try:
				newSoireeVide.save()
				message = u"La soirée du<a href='/soirees/"+date+"'><b> " + date + u"</b></a> a bien été ajouté dans la base"
				return saisie(request, active_tab='Soiree',alert='on',alert_type='success',alert_message=message)
			except ValidationError as e:
				message = ' '.join(e.messages)
				return saisie(request, active_tab='Soiree',alert='on',alert_type='danger',alert_message=message,
			  previous_values = request.POST)
			except IntegrityError:
				message = 'Une soiree utilise déjà cette page de registre'
				return saisie(request, active_tab='Soiree',alert='on',alert_type='danger',alert_message=message,
			  previous_values = request.POST)
	else :
		message = u"La soirée du<a href='/soirees/"+date+"'><b> " + date + u"</b></a> a déjà été enregistrer comme une soirée avec des information, si c'est une erreur veuillez supprimer cette <a href='/soirees/"+date+u"'>soirée</a>"
		return saisie(request, active_tab='Soiree',alert='on',alert_type='danger',alert_message=message)
			
			

@login_required(login_url='/login/')
def update(request, type, id) :
	instance = {}
	if type == 'personne':
		instance['personneForm'] = model_to_dict(Personne.objects.get(id=id))
		instance['personneForm']['personneForm_id'] = id	
	elif type == 'piece':
		instance['pieceForm'] = model_to_dict(Piece.objects.get(id=id))
		instance['pieceForm']['pieceForm_id'] = id	
	else :
		soiree = Soiree.objects.get(id=id)
		instance['soireeForm'] = model_to_dict(soiree)
		instance['soireeForm']['soireeForm_id'] = id
		instance['soireeForm'].update(model_to_dict(soiree.page_registre))
		instance['soireeForm'].update(model_to_dict(soiree.budget))
		instance['soireeForm']['budget_id'] = soiree.budget.id
		instance['soireeForm']['credit_final_reg'] = numberToCurrency(soiree.budget.credit_final_reg)
		instance['soireeForm']['debit_initial_reg'] = numberToCurrency(soiree.budget.debit_initial_reg)
#		instance['soireeForm']['montant_cachet'] = numberToCurrency(soiree.budget.montant_cachet)
		instance['soireeForm']['montant_cachet_auteur'] = numberToCurrency(soiree.budget.montant_cachet_auteur)
		instance['soireeForm']['quart_pauvre_reg'] = numberToCurrency(soiree.budget.quart_pauvre_reg)
		instance['soireeForm']['reste_reg'] = numberToCurrency(soiree.budget.reste_reg)
		instance['soireeForm']['total_depenses_reg'] = numberToCurrency(soiree.budget.total_depenses_reg)
		instance['soireeForm']['total_recettes_reg'] = numberToCurrency(soiree.budget.total_recettes_reg)
		instance['soireeForm']['debit_derniere_soiree_reg'] = numberToCurrency(soiree.budget.debit_derniere_soiree_reg)
		instance['soireeForm']['total_depenses_corrige_reg'] = numberToCurrency(soiree.budget.total_depenses_corrige_reg)	
		
		representations = Representation.objects.all().filter(Soiree=soiree)
		i = 0
		for representation in representations :
			instance['soireeForm'].update({ 'representation'+str(i)+k:v for k,v in model_to_dict(representation).iteritems() })	
			instance['soireeForm']['representation'+str(i)+'id'] = representation.id
			i += 1	
		animations = Animation.objects.all().filter(Soiree=soiree)
		i = 0
		for animation in animations :
			instance['soireeForm'].update({ 'animation'+str(i)+k:v for k,v in model_to_dict(animation).iteritems() })
			instance['soireeForm']['animation'+str(i)+'id'] = animation.id
			i += 1	
		roles = Role.objects.all().filter(representation__Soiree=soiree)
		i = 0
		for role in roles :
			instance['soireeForm'].update({ 'role'+str(i)+k:v for k,v in model_to_dict(role).iteritems() })
			instance['soireeForm']['role'+str(i)+'id'] = role.id
			i += 1				
		debits = Debit.objects.all().filter(budget=soiree.budget)
		i = 0
		for debit in debits :
			instance['soireeForm'].update({ 'debit'+str(i)+k:v for k,v in model_to_dict(debit).iteritems() })
			instance['soireeForm']['debit'+str(i)+'id'] = debit.id
			instance['soireeForm']['debit'+str(i)+'montant'] = numberToCurrency(debit.montant)
			i += 1		
		billetteries = Billetterie.objects.all().filter(budget=soiree.budget)
		i = 0
		for billetterie in billetteries :
			instance['soireeForm'].update({ 'billetterie'+str(i)+k:v for k,v in model_to_dict(billetterie).iteritems() })
			instance['soireeForm']['billetterie'+str(i)+'id'] = billetterie.id
			instance['soireeForm']['billetterie'+str(i)+'montant'] = numberToCurrency(billetterie.montant)
			i += 1
		credits = Credit.objects.all().filter(budget=soiree.budget).exclude(id__in=billetteries)
		i = 0
		for credit in credits :
			instance['soireeForm'].update({ 'credit'+str(i)+k:v for k,v in model_to_dict(credit).iteritems() })
			instance['soireeForm']['credits'+str(i)+'id'] = credits.id
			instance['soireeForm']['credits'+str(i)+'montant'] = numberToCurrency(credits.montant)
			i += 1		
			
	return saisie(request,active_tab=type.capitalize(), previous_values=instance)

@login_required(login_url='/login/')
def delete(request, type, id):
	if type == "personne":
		personne = Personne.objects.get(id=id)
		personne.delete()
	elif type == "piece":
		piece = Piece.objects.get(id=id)
		piece.delete()
	else:
		soiree = Soiree.objects.get(id=id)
		budget = soiree.budget
		representations = Representation.objects.all().filter(Soiree=soiree)
		for representation in representations :
			representation.delete()
		animations = Animation.objects.all().filter(Soiree=soiree)
		for animation in animations :
			animation.delete()
		debits = Debit.objects.all().filter(budget=soiree.budget)
		for debit in debits :
			debit.delete()
		billetteries = Billetterie.objects.all().filter(budget=soiree.budget)
		for billetterie in billetteries :
			billetterie.delete()
		credits = Credit.objects.all().filter(budget=soiree.budget).exclude(id__in=billetteries)
		for credit in credits :
			credit.delete()
		soiree.delete()
		budget.delete()
	return HttpResponseRedirect('/'+type+'s')
	

# Permet la mise en forme des champs date listé (list_champs_date) dans un dictionnaire donné (data)	  
def testDateForm(data, list_champs_date) :
	for champs_date in list_champs_date:
		date = data[champs_date]
		data[champs_date+'_isComplete'] = True
		dateTextIsBlank = True
		if '?' in date:
			data[champs_date+'_text'] = date
			data[champs_date+'_isComplete'] = False
			dateTextIsBlank = False
			date = date.replace(u'?',u'0')
			date = date.replace(u'.',u'0')
		if re.match(r'^\d{4}$',date, re.UNICODE):
			if dateTextIsBlank :
				data[champs_date+'_text'] = date
				data[champs_date+'_isComplete'] = False
				dateTextIsBlank = False
			date += '-01-01'
			data[champs_date] = date
		if re.match(r'^[\w,û,é]* \d{4}$',date, re.UNICODE):
			if dateTextIsBlank :
				data[champs_date+'_text'] = date
				data[champs_date+'_isComplete'] = False
				dateTextIsBlank = False
			date = '01 '+date
		if re.match(r'^\d{1,2} [\w,û,é]* \d{4}$',date, re.UNICODE):
			date = date.replace(u'janvier',u'01')
			date = date.replace(u'février',u'02')
			date = date.replace(u'mars',u'03')
			date = date.replace(u'avril',u'04')
			date = date.replace(u'mai',u'05')
			date = date.replace(u'juin',u'06')
			date = date.replace(u'juillet',u'07')
			date = date.replace(u'août',u'08')
			date = date.replace(u'septembre',u'09')
			date = date.replace(u'octobre',u'10')
			date = date.replace(u'novembre',u'11')
			date = date.replace(u'décembre',u'12')
			date = date[-4:] + '-' + date[date.index(' ')+1:-5] + '-' + date[:date.index(' ')]
			data[champs_date] = date
		if not re.match(r'^\d{4}-\d{1,2}-\d{1,2}$',date, re.UNICODE):
			if dateTextIsBlank :
				data[champs_date+'_text'] = date
				data[champs_date+'_isComplete'] = False
				dateTextIsBlank = False
			data[champs_date] = '1700-01-01'			
	return data