#-*- coding: utf-8 -*-
import csv
import sys
import os.path
import codecs
import re
from io import TextIOWrapper
from datetime import date
import logging
import pdb

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from importcsv.models import Document
from importcsv.forms import DocumentForm
from django.shortcuts import get_object_or_404, render, render_to_response
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

from navigation.models import *
from importcsv.models import *
from saisie.forms import *

import regital.settings
import locale


class CSVParser:
	def __init__(self):
		#csvfile = open('importcsv/db_regital_v4.csv', 'rb')
		self.info = "\nParsing effectue"
		print >>sys.stderr, "\nINFO : Open effectue"
		#dialect = csv.Sniffer().sniff(codecs.EncodedFile(csvfile,"utf-8").read(1024))
		#dialect = csv.Sniffer().sniff(f.read(1024))
		#csvfile.seek(0) # seek to 0
		
		self.reader = csv.reader(csvfile, delimiter=';')
		fieldnames = ['_a_ref_registre', '_b_num_page_pdf', '_c_titre', '_d_titre_brenner', '_e_langue', '_f_jour', '_g_num', '_h_mois', '_i_annee', '_j_auteur',
			'_k_premiere', '_l_depense_div', '_m_traduction', '_n_mots_clefs', '_o_montant_depense_div', '_p_depense_ord', '_q_instruments', '_r_animaux',
			'_s_coiffeuse', '_t_picard', '_u_buron', '_v_M. Sticotti', '_w_coffre-fort', '_x_Nicolo et/ou Villars', '_y_spese extra',
			'_z_sconba', 'aa_putella', 'ab_lista', 'ac_chaises', 'ad_porteur', 'ae_carrosse', 'af_habilleur', 'ag_menuisier De Lande', 'ah_afficheur',
			'ai_gardes', 'aj_souffleur', 'ak_lustres', 'al_perruquier', 'am_hommes ou enfants en plus', 'an_bougies', 'ao_arguments', 'ap_mances',
			'aq_danseurs', 'ar_pour le feu', 'as_total_depenses_reg', 'at_debit_derniere_soiree_reg', 'au_balcon_premiere', 'av_recette_balcon_premiere',
			'aw_balcon_deuxieme', 'ax_recette_balcon_deuxieme', 'ay_premiere', 'az_recette_premiere', 'ba_deuxieme', 'bb_recette_deuxieme',
			'bc_troisieme', 'bd_recette_troisieme', 'be_parterre', 'bf_recette_parterre', 'bg_prima_loggia', 'bh_recette_prima_loggia',
			'bi_seconda_loggia', 'bj_recette_seconda_loggia', 'bk_personnalite', 'bl_recette_personnalite', 'bm_supplement', 'bn_recette_supplement',
			'bo_paradis', 'bp_recette_paradis', 'bq_nb_total_billets_vendus_reg', 'br_total_recettes_reg', 'bs_quart_pauvre_reg', 'bt_total_depenses_corrige_reg',
			'bu_debit_initial_reg', 'bv_reste_reg', 'bw_credit', 'bx_credit_final_reg', 'by_r_debit_total_reg', 'bz_r_credit_total_reg', 'ca_montant_cachet_auteur',
			'cb_cachet_6', 'cc_cachet_9', 'cd_cachet_12', 'ce_cachet_12¼', 'cf_cachet_12½', 'cg_cachet_13', 'ch_cachet_13¾', 'ci_cachet_14', 'cj_cachet_14¾', 'ck_cachet_15',
			'cl_anecdote', 'cm_redacteur']
		self.report = {'row_count': 0, 'warning': 0, 'error': 0}
		self.database = csv.DictReader(csvfile, dialect=csv.excel_tab, fieldnames=fieldnames, delimiter=';')
		self.fieldmapping = next(self.database)
		logging.debug(self.fieldmapping)

		'''for ligne1 in self.database:
			for ligne2 in fieldnames:
				print >>sys.stderr, "\nDATA: "+str(ligne2)+":"+str(ligne1[ligne2])
			print >>sys.stderr, "\nNEXT:"
		'''

		self.context = {'pageregistre': None, 'soiree': None, 'budgetsoiree': None, 'piece': None}

	def bulk_insert(self):
		#from collections import OrderedDict
		i = 1
		for row in self.database:
			i += 1
			print >>sys.stderr, "\nINFO : bulk_insert ligne"+str(i)+" de "+str(row['_a_ref_registre'])
			print('[{}]'.format(self.database.line_num),)
			sys.stdout.flush()
			self._insert_row(row)
			self.report['row_count']+=1
	#		if self._tov(row['TOTAL_DEPENSES']) >= self._tov('150'):
	#			print('Dépenses de {!r}: {}'.format(row['TITRE_PIECE'], self._tos(self._tov(row['TOTAL_DEPENSES']))))
					
		'''conversion de la monnaie au format "livre, sou, denier" ou "livre, sou"
		vers denier au format numérique (entier).
		règles de conversion de la monnaie de l'Ancien Régime : 1 livre (£) = 20 sous (S) = 240 deniers (d)
		'''
	def _tov(self, s):
		#print >>sys.stderr, "\nINFO : _tov(self, s)"
		if not s: return 0	# valeur vide ANCIENNE VERSION -> /!\ retourne un char plutôt qu'un int...
		if not re.match('^(\d+)(,\d+)*(,|_)?$', s):
			logging.error('[{}] Erreur       : format de valeur monétaire inconnu pour {!r}'.format(self.database.line_num, s))
			self.report['error']+=1
			return -1	# format non reconnu
		
		tokens = re.findall('\d+', s)
		val = 0
		if len(tokens)==1:		# format £
			val = 240*int(tokens[0])
		elif len(tokens)==2:		# format £,S
			val = 240*int(tokens[0]) + 12*int(tokens[1])
		elif len(tokens)==3:	# format £,S,d
			val = 240*int(tokens[0]) + 12*int(tokens[1]) + int(tokens[2])
		else: return -1 	# format non reconnu
		return val
			
	def _tos(self, v):
		#print >>sys.stderr, "\nINFO : _tos(self, v)"
		if not v: return ''
		if v>=0:	# valeur monétaire
			li, v = divmod(v, 240)
			s, d = divmod(v, 12)
			if d > 0: 
				sval = '{!s}£ {!s}S {!s}d'.format(li, s, d)
			elif s > 0: 
				sval = '{!s}£ {!s}S'.format(li, s)
			else: 
				sval = '{!s}£'.format(li)
			return sval
		else: 
			logging.error('[{}] Erreur       : valeur monétaire {!r} impropre'.format(self.database.line_num, v))
			return '?!'	# erreur

	'''procédure d'importation d'une ligne dans la base de données'''
	def _insert_row(self, row):
		print >>sys.stderr, "\nINFO : _insert_row(self, row)"
		
		# RESET du context.soiree et budget soiree
		#self.context['soiree'] = None
		#self.context['budgetsoiree'] = None
		print >>sys.stderr, "INFO: Verif de context soiree: "+str(self.context['soiree'])+" et budget: "+str(self.context['budgetsoiree'])

		# registre
		self._insert_pageregistre(row)
		
		# budget de la soirée
		self._insert_budgetsoiree(row)

		# soirée
		self._insert_soiree(row)
		
		# billetterie
		self._insert_billetterie(row)
		# dépense
		self._insert_depense(row)
		# piece
		self._insert_piece(row)


	def _insert_piece(self, row):
		print >>sys.stderr, "\nINFO : _insert_piece(self, row)"
		if not row['_i_annee']: # aucune pièce déclarée à cette ligne \!/ on utilise la présence d'une date pour détecter la déclaration d'une pièce 
			return None
		if not row['_c_titre']:
			logging.error('[{}] Erreur       : aucune pièce n''est déclarée'.format(self.database.line_num))
			self.report['error']+=1
			return None
		
		print >>sys.stderr, "	row['_c_titre'] "
		print >>sys.stderr, row['_c_titre']
		pieces = row['_c_titre'].replace('_', ' ').strip().split('/')
		b_pieces = row['_d_titre_brenner'].replace('_', ' ').strip().split('/')
		auteurs = row['_j_auteur'].replace('_', ' ').strip().split(';')

		langs = row['_e_langue'].replace('_','').strip().lower().split(';')
		if (len(pieces)>len(langs)):
			for i in range(len(pieces)-1):
				langs.append(langs[0])

		prems = row['_k_premiere'].strip().split(';')
		print>>sys.stderr, "	INFO : pieces:"+str(pieces)+" b_pieces:"+str(b_pieces)+" auteurs:"+str(auteurs)+" langs:"+str(langs)+" prems:"+str(prems)

		if (len(pieces)!=len(b_pieces) or len(pieces)!=len(langs) or len(pieces)!=len(prems) or len(pieces)!=len(auteurs)):
			logging.error('[{}] Erreur       : le nombre de pièces est incompatible'.format(self.database.line_num))
			self.report['error']+=1
			print>>sys.stderr, "	ERR : Le nombre de pièces est incompatible"
			return None
			
		for i in range(len(pieces)):
			print>>sys.stderr, "	INFO : pieces[i]:"+str(pieces[i])+" b_pieces[i]:"+str(b_pieces[i])+" auteurs[i]:"+str(auteurs[i])
			rec = {}
			rec['titre'] = pieces[i]
			rec['titre_brenner'] = b_pieces[i]
			if len(prems[i]) <= 8:	# manque le siècle (18e) pour l'année. (34 complété à 2034 au lieu de 1734)
				 rec['date_premiere']= prems[i][:6]+'17'+prems[i][6:]
			else:
				rec['date_premiere'] = prems[i]
			rec['langue'] = langs[i]
			
			new_piece = None
			
			form = PieceForm(rec)
#			pdb.set_trace()
			try:
				form.is_valid()
			except (ValueError, ValidationError) as e:
				logging.error('[{}] Erreur       : {}'.format(self.database.line_num, e))
				self.report['error']+=1
			else:		
				try:
					new_piece= form.save(commit=True)
				except ValueError as e:
					try:
						piece_fetch = Piece.objects.get(titre=rec['titre'])
						representationform = { 'position': i+1 , 'Soiree': self.context['soiree'].id , 'piece': piece_fetch.id}
						print >>sys.stderr, "	INFO : representationform"+str(representationform)
						form = RepresentationFormInputs(representationform) 
						if form.is_valid():
							print>>sys.stderr, "	INFO : NEW REPRESENTATION 1"
							form.save()
						else:
							print>>sys.stderr, "	ERR : Form REPRESENTATION non valide 1"
					except Piece.DoesNotExist as errors:
						print>>sys.stderr, "	ERR : Aucune piece trouvée"

					logging.error('[{}] Erreur        : {}'.format(self.database.line_num, e))
					self.report['error']+=1
				except (ValidationError, IntegrityError) as e: # la pièce est déjà enregistrée !
					try:
						piece_fetch = Piece.objects.get(titre=rec['titre'])
						representationform = { 'position': i+1 , 'Soiree': self.context['soiree'].id , 'piece': piece_fetch.id}
						form = RepresentationFormInputs(representationform) 
						if form.is_valid():
							print>>sys.stderr, "	INFO : NEW REPRESENTATION 2"
							form.save()
						else:
							print>>sys.stderr, "	ERR : Form REPRESENTATION non valide 2"
					except Piece.DoesNotExist as errors:
						print>>sys.stderr, "	ERR : Aucune piece trouvée"
					logging.error('[{}] Erreur       : {}'.format(self.database.line_num, e))
					self.report['error']+=1
				else:	
					self.context['piece']= new_piece
					self.__insert_auteurs(auteurs[i])
					print >>sys.stderr, "AVANT"
					self.context['piece'].save()
					print >>sys.stderr, "APRES"
					representationform = { 'position': i+1 , 'Soiree': self.context['soiree'].id , 'piece': self.context['piece'].id}
					form = RepresentationFormInputs(representationform) 
					if form.is_valid():
						print>>sys.stderr, "	INFO : NEW REPRESENTATION 3"
						form.save()
					else:
						print>>sys.stderr, "	ERR : Form REPRESENTATION non valide 3"
					#self.context['piece'].save_m2m()
		

		return new_piece

	def __insert_auteurs(self, auteurs):
		print >>sys.stderr, "\nINFO : __insert_auteurs(self, "+str(auteurs)+")"
		if not auteurs:
			logging.warning('[{}] Attention    : aucun auteur déclaré pour {}'.format(self.database.line_num, self.context['piece']))
			self.report['warning'] +=1
			return None

		auts = auteurs.split('/')
		for nom in auts:	# pour chaque auteur
#			new_personne = None
			rec = {'nom': nom, 'prenom': '', 'genre': '-', 'nationalite': '-'}
			try:
				new_personne = Personne.objects.get(**rec)
			except Personne.DoesNotExist as e:
				form = PersonneForm(rec)
				try:
					form.is_valid()
				except (ValueError, ValidationError) as e:
					logging.error('[{}] Erreur       : {}'.format(self.database.line_num, e))
					self.report['error']+=1
				else:				
					new_personne = form.save(commit=True)
			if new_personne:
				self.context['piece'].auteurs.add(new_personne.pk)
		return True

	def _insert_depense(self, row):
		print >>sys.stderr, "\nINFO : _insert_depense(self, row)"
		if not self.context['budgetsoiree']:
			try:
				self.context['budgetsoiree'] = BudgetSoiree.objects.get(soiree=self.context['soiree'])
			except BudgetSoiree.DoesNotExist as e:
				logging.error('[{}] Erreur       : {}'.format(self.database.line_num, e))
				self.report['error']+=1
				return None

		if row['_l_depense_div']:
			self.__insert_ligne_debit(
				row['_l_depense_div'].replace('_', ' ').strip(),
				self._tov(row['_o_montant_depense_div'].strip()),
				4,
				row['_m_traduction'].replace('_', ' ').strip(),
				row['_n_mots_clefs'].replace('_', ' ').strip()
			)
			
		if row['_p_depense_ord']:
			self.__insert_ligne_debit(
				'-',
				self._tov(row['_p_depense_ord'].strip()),
				0
			)

			# clés de prefixe _q à ar...
			key_dep = [x for x in row.keys() if re.match('(_[q-z]|a[a-r])', x)]
			print >>sys.stderr, 'KEY_DEP: '+str(key_dep)
			for k in key_dep:
				if row[k]:
					self.__insert_ligne_debit(
						k[3:],
						self._tov(row[k].strip())
					)
					
	def __insert_ligne_debit(self, lib, montant, t_depense=5, trad='', mots_clefs=''):
		print >>sys.stderr, "	INFO : __insert_ligne_debit(self, "+str(lib)+", "+str(montant)+", "+str(t_depense)+", "+str(trad)+", "+str(mots_clefs)+")"
		rec = {}
		new_debit = None
		rec['libelle'] = lib
		rec['montant'] = montant
		rec['type_depense'] = t_depense
		rec['traduction'] = trad
		rec['mots_clefs'] = mots_clefs
		form = DebitFormInputs(rec)
		print >>sys.stderr, "		ERR : form ligne debit "+str(form.errors)
		try:
			form.is_valid()
		except ValidationError as e:
#			print('{}'.format(rec))
			logging.error('[{}] Erreur       : {}'.format(self.database.line_num, e))
			self.report['error']+=1
		else:
			new_debit = form.save(commit=False)
			new_debit.budget = self.context['budgetsoiree']
			try:
				new_debit = form.save(commit=True)
			except (ValidationError, IntegrityError) as e: # la dépense est déjà enregistrée !
#				logging.error('[{}] Erreur       : {}'.format(self.database.line_num, e))
#				self.report['error']+=1
				pass
			except ValueError as e:
#				print('{}'.format(rec))
				logging.error('[{}] Erreur       : {}'.format(self.database.line_num, e))
				self.report['error']+=1
		return new_debit
		
	def __insert_redacteurs(self, row):
		print >>sys.stderr, "\nINFO : __insert_redacteurs(self, row)"
		# tous les contrôles sont opérés à partir de _insert_budgetsoiree
##		if self.context['budgetsoiree'].redacteurs: # rédacteur déjà enregistré pour la soirée courante 
##			return None
		if not row['cm_redacteur']:
			logging.warning('[{}] Attention    : aucun rédacteur déclaré pour {}'.format(self.database.line_num, self.context['budgetsoiree']))
			self.report['warning'] +=1
			return None
		
		reds = row['cm_redacteur'].split('/')
		for nom in reds:	# pour chaque rédacteur
#			new_personne = None
			rec = {'nom': nom, 'prenom': '', 'genre': '-', 'nationalite': '-'}
			try:
				new_personne = Personne.objects.get(**rec)
			except Personne.DoesNotExist as e:
				form = PersonneForm(rec)
				try:
					form.is_valid()
				except (ValueError, ValidationError) as e:
					logging.error('[{}] Erreur       : {}'.format(self.database.line_num, e))
					self.report['error']+=1
				else:
					print >>sys.stderr, "INFO: ERR sur form Personne -> "+str(form.errors)				
					new_personne = form.save(commit=True)
			if new_personne:
				self.context['pageregistre'].redacteurs.add(new_personne)
		return True
		

	def _insert_budgetsoiree(self, row):
		print >>sys.stderr, "\nINFO : _insert_budgetsoiree(self, row)"
		rec = {}
		new_budgetsoiree = None

		mois=0
		print >>sys.stderr, "	INFO : row['_h_mois'] "+row['_h_mois']
		if not row['_h_mois']: pass
		elif row['_h_mois'].strip().lower() in ['1', 'gennaro', 'genaro', 'gienaro', 'gen°', 'gen¬_', 'janvier', 'jan']: mois=1
		elif row['_h_mois'].strip().lower() in ['2', 'febrario', 'febraro', 'febro', 'février', 'fevrier', 'feb']: mois=2
		elif row['_h_mois'].strip().lower() in ['3', 'marzo', 'mars', 'mar']: mois=3
		elif row['_h_mois'].strip().lower() in ['4', 'aprile', 'ape', 'avril', 'apr']: mois=4
		elif row['_h_mois'].strip().lower() in ['5', 'maggio', 'magg°', 'mag°','mag¬_', 'magg¬_', 'mai', 'may']: mois=5
		elif row['_h_mois'].strip().lower() in ['6', 'giugno', 'zugg°', 'zugg¬_', 'zug°', 'zug¬_', 'juin', 'jun']: mois=6
		elif row['_h_mois'].strip().lower() in ['7', 'luglio', 'lugg°', 'lug°', 'lugl°', 'lug¬_', 'lugg¬_', 'lugl¬_', 'juillet', 'jul']: mois=7
		elif row['_h_mois'].strip().lower() in ['8', 'agosto', 'agto', 'agt°', 'agt¬_', 'août', 'aout', 'aug']: mois=8
		elif row['_h_mois'].strip().lower() in ['9', 'settembre', 'setembre', '7bre', 'se', 'septembre', 'sep']: mois=9
		elif row['_h_mois'].strip().lower() in ['10', 'ottobre', 'otobre', 'ottombre', '8bre', 'otto', 'octobre', 'oct']: mois=10
		elif row['_h_mois'].strip().lower() in ['11', 'novembre', 'novbre', '9bre', 'nov']: mois=11
		elif row['_h_mois'].strip().lower() in ['12', 'decembre', 'xmbre', 'xbre', '10bre', 'dto', 'detto', 'décembre', 'dec']: mois=12
		else:
			logging.error('[{}] Erreur       : Le mois {!r} est inconnu'.format(self.database.line_num, row['_h_mois']))
			self.report['error']+=1

		print >>sys.stderr, "	INFO: row['_g_num'] and mois!=0 and row['_i_annee']: "+str(row['_g_num'])+" "+str(mois)+" "+str(row['_i_annee'])
		if row['_g_num'] and mois!=0 and row['_i_annee']:
			test_date='{}-{}-{}'.format(row['_i_annee'].strip(), mois, row['_g_num'].strip())

			print >>sys.stderr, "	INFO: Test de context soiree: "+str(self.context['soiree'])+" et budget: "+str(self.context['budgetsoiree'])
			if self.context['soiree']:
				print >>sys.stderr, "INFO: test_date "+test_date
				if self.context['soiree'].date == test_date:
					if self.context['soiree'].budget:	# la soirée et son budget sont déjà enregistrés !
						print >>sys.stderr, "INFO : # la soirée et son budget sont déjà enregistrés !"
						self.context['budgetsoiree'] = self.context['soiree'].budget
						return None
			else:
				print >>sys.stderr, "	INFO: _insert_budgetsoiree dans context soiree pass"
				pass
		
		if row['as_total_depenses_reg']:	# la ligne définit bien un budget de soirée, c'est parti !
			rec['total_depenses_reg'] = self._tov(row['as_total_depenses_reg'].strip())
			# /!\ ERREUR DE LIGNE DANS LE CSV OU LE NB TOTAL EST PAS OU MAL INDIQUE
			if row['bq_nb_total_billets_vendus_reg'].strip()=='' or row['bq_nb_total_billets_vendus_reg'].strip()=='Imp.':
				rec['nb_total_billets_vendus_reg'] = -1
			else:
				rec['nb_total_billets_vendus_reg'] = int(row['bq_nb_total_billets_vendus_reg'].strip())
			rec['total_recettes_reg'] = self._tov(row['br_total_recettes_reg'].strip())
			# teste si CREDIT (BW) = RECETTES_BILLETS_VENDUS (BR)	
			if not rec['total_recettes_reg'] == self._tov(row['bw_credit'].strip()):
				logging.warning('[{}] Avertissement: {!r} (crédit BW) <> {!r} (recette billets BR)'.format(
					self.database.line_num,
					self._tos(self._tov(row['bw_credit'].strip())),
					self._tos(rec['total_recettes_reg']),
				))
				self.report['warning']+=1

			rec['debit_derniere_soiree_reg'] = self._tov(row['at_debit_derniere_soiree_reg'].strip())	# report à vérifier
			rec['total_depenses_corrige_reg'] = self._tov(row['bt_total_depenses_corrige_reg'].strip())
			# teste si dépenses corrigées = dépenses + débit dernière soirée
			dep_corrigee = rec['total_depenses_reg']
			if rec['debit_derniere_soiree_reg']:
				dep_corrigee += rec['debit_derniere_soiree_reg']
			if not rec['total_depenses_corrige_reg'] == dep_corrigee:
				logging.warning('[{}] Avertissement: {!r} (dépense corrigée) <> {!r} (dépense) + {!r} (report)'.format(
					self.database.line_num,
					self._tos(rec['total_depenses_corrige_reg']),
					self._tos(rec['total_depenses_reg']),
					self._tos(rec['debit_derniere_soiree_reg']),
				))
				self.report['warning']+=1
				
			rec['quart_pauvre_reg'] = self._tov(row['bs_quart_pauvre_reg'].strip())
			rec['debit_initial_reg'] = self._tov(row['bu_debit_initial_reg'].strip())
			# teste si débit initial = quart du pauvre + total des dépenses corrigé [valeurs déclarées]
			if (not rec['quart_pauvre_reg'] or
				not rec['total_depenses_corrige_reg'] or
				not rec['debit_initial_reg'] or
				not rec['debit_initial_reg'] == rec['quart_pauvre_reg'] + rec['total_depenses_corrige_reg']):
				logging.warning('[{}] Avertissement: {!r} (débit initial) <> {!r} (quart du pauvre) + {!r} (dépense corrigée)'.format(
					self.database.line_num,
					self._tos(rec['debit_initial_reg']),
					self._tos(rec['quart_pauvre_reg']),
					self._tos(rec['total_depenses_corrige_reg']),
				))
				self.report['warning']+=1
			
			rec['reste_reg'] = self._tov(row['bv_reste_reg'].strip())
			# teste si reste = |recette billets - débit initial| (valeur absolue) [valeurs déclarées]
			if (not rec['reste_reg'] or
				not rec['total_recettes_reg'] or
				not rec['debit_initial_reg'] or
				not rec['reste_reg'] == abs(rec['total_recettes_reg'] - rec['debit_initial_reg'])):
				logging.warning('[{}] Avertissement: {!r} (reste) <> |{!r} (recettes) - {!r} (débit initial)|'.format(
					self.database.line_num,
					self._tos(rec['reste_reg']),
					self._tos(rec['total_recettes_reg']),
					self._tos(rec['debit_initial_reg']),
				))
				self.report['warning']+=1
			
			# Plus utilisé dans le models.py actuel (mai 2014)
			# rec['r_debit_total_reg'] = self._tov(row['by_r_debit_total_reg'].strip())
			# rec['r_credit_total_reg'] = self._tov(row['bz_r_credit_total_reg'].strip())
			
			print>>sys.stderr, "	INFO : Insertion cachet"
			if row['cb_cachet_6']:
				rec['montant_cachet'] = 1440
				rec['nombre_cachets'] = float(row['cb_cachet_6'].strip().replace(',','.'))
			elif row['cc_cachet_9']:
				rec['montant_cachet'] = 2160
				rec['nombre_cachets'] = float(row['cc_cachet_9'].strip().replace(',','.'))
			elif row['cd_cachet_12']:
				rec['montant_cachet'] = 2880
				print>>sys.stderr, "	INFO : row['cd_cachet_12'] "+str(row['cd_cachet_12'])
				nombre_cachets_res = row['cd_cachet_12'].strip().replace(',','.')
				nombre_cachets_split = re.split('.',nombre_cachets_res)
				print>>sys.stderr, nombre_cachets_res
				print>>sys.stderr, nombre_cachets_split
				if(len(nombre_cachets_split)<2 or nombre_cachets_split[0]==''):
					rec['nombre_cachets'] = float(row['cd_cachet_12'].strip().replace(',','.'))
				else:
					nombre_cachets_split_final = float(int(nombre_cachets_split[0]))+0.1*float(int(nombre_cachets_split[1]))
					rec['nombre_cachets'] = float(nombre_cachets_split_final)
				#rec['nombre_cachets'] = float(row['cd_cachet_12'].strip().replace(',','.'))
			elif row['ce_cachet_12¼']:
				rec['montant_cachet'] = 2940
				print>>sys.stderr, "	INFO : row['ce_cachet_12¼'] "+str(row['ce_cachet_12¼'])
				nombre_cachets_res = row['ce_cachet_12¼'].strip().replace(',','.')
				nombre_cachets_split = re.split('.',nombre_cachets_res)
				print>>sys.stderr, nombre_cachets_res
				print>>sys.stderr, nombre_cachets_split
				if(len(nombre_cachets_split)<2 or nombre_cachets_split[0]==''):
					rec['nombre_cachets'] = float(row['ce_cachet_12¼'].strip().replace(',','.'))
				else:
					nombre_cachets_split_final = float(int(nombre_cachets_split[0]))+0.1*float(int(nombre_cachets_split[1]))
					rec['nombre_cachets'] = float(nombre_cachets_split_final)
			elif row['cf_cachet_12½']:
				rec['montant_cachet'] = 3000
				print>>sys.stderr, "	INFO : row['cf_cachet_12½'] "+str(row['cf_cachet_12½'])
				nombre_cachets_res = row['cf_cachet_12½'].strip().replace(',','.')
				nombre_cachets_split = re.split('.',nombre_cachets_res)
				print>>sys.stderr, nombre_cachets_res
				print>>sys.stderr, nombre_cachets_split
				if(len(nombre_cachets_split)<2 or nombre_cachets_split[0]==''):
					rec['nombre_cachets'] = float(row['cf_cachet_12½'].strip().replace(',','.'))
				else:
					nombre_cachets_split_final = float(int(nombre_cachets_split[0]))+0.1*float(int(nombre_cachets_split[1]))
					rec['nombre_cachets'] = float(nombre_cachets_split_final)
			elif row['cg_cachet_13']:
				rec['montant_cachet'] = 3120
				print>>sys.stderr, "	INFO : row['cg_cachet_13'] "+str(row['cg_cachet_13'])
				nombre_cachets_res = row['cg_cachet_13'].strip().replace(',','.')
				nombre_cachets_split = re.split('.',nombre_cachets_res)
				print>>sys.stderr, nombre_cachets_res
				print>>sys.stderr, nombre_cachets_split
				if(len(nombre_cachets_split)<2 or nombre_cachets_split[0]==''):
					rec['nombre_cachets'] = float(row['cg_cachet_13'].strip().replace(',','.'))
				else:
					nombre_cachets_split_final = float(int(nombre_cachets_split[0]))+0.1*float(int(nombre_cachets_split[1]))
					rec['nombre_cachets'] = float(nombre_cachets_split_final)
			elif row['ch_cachet_13¾']:
				rec['montant_cachet'] = 3300
				print>>sys.stderr, "	INFO : row['ch_cachet_13¾'] "+str(row['ch_cachet_13¾'])
				nombre_cachets_res = row['ch_cachet_13¾'].strip().replace(',','.')
				print>>sys.stderr, nombre_cachets_res
				nombre_cachets_split = nombre_cachets_res.split('.')
				print>>sys.stderr, nombre_cachets_split
				if(len(nombre_cachets_split)<2 or nombre_cachets_split[0]==''):
					rec['nombre_cachets'] = float(row['ch_cachet_13¾'].strip().replace(',','.'))
				else:
					nombre_cachets_split_final = float(int(nombre_cachets_split[0]))+0.1*float(int(nombre_cachets_split[1]))
					rec['nombre_cachets'] = nombre_cachets_split_final
					print>>sys.stderr, "	INFO : rec['nombre_cachets'] "+str(rec['nombre_cachets'])
					
			elif row['ci_cachet_14']:
				rec['montant_cachet'] = 3360
				rec['nombre_cachets'] = float(row['ci_cachet_14'].strip().replace(',','.'))
			elif row['cj_cachet_14¾']:
				rec['montant_cachet'] = 3540
				rec['nombre_cachets'] = float(row['cj_cachet_14¾'].strip().replace(',','.'))
			elif row['ck_cachet_15']:
				rec['montant_cachet'] = 3600
				rec['nombre_cachets'] = float(row['ck_cachet_15'].strip().replace(',','.'))
			else:
				rec['montant_cachet'] = -1
				rec['nombre_cachets'] = ''
			
			rec['montant_cachet_auteur'] = self._tov(row['ca_montant_cachet_auteur'].strip())
			rec['credit_final_reg'] = self._tov(row['bx_credit_final_reg'].strip())
			
			form = BudgetSoireeFormInputs(rec)

			#print >>sys.stderr, "REC : "+str(rec)
			#print >>sys.stderr, "\nTYPES : "
			#for rowprint in rec:
			#	print >>sys.stderr, rowprint+" -> "+str(format(type(rec.get(rowprint))))+" -> "+str(rec[rowprint])

			if form.is_valid():
				print >>sys.stderr, "	INFO : NEW BUDGET SOIREE "
				new_budgetsoiree= form.save(commit=True)	# premier commit pour utiliser la relation ManyToMany des rédacteurs
				self.context['budgetsoiree'] = new_budgetsoiree
				# insertion des rédacteurs
				self.__insert_redacteurs(row)	# ajoute les rédacteurs du budget de la soirée en cours
				new_budgetsoiree.save() # second commit, avec les rédacteurs -- à optimiser avec "update"
				
				#print ('.', end='')
			else:
				print >>sys.stderr, "	ERR : form de budgetSoiree non valide "
				print >>sys.stderr, form.errors
				logging.error('[{}] Erreur       : {}'.format(self.database.line_num, form.errors))
				self.report['error']+=1
		else:	# pas de budget de soirée à cette ligne
			pass
		return new_budgetsoiree


	def _insert_billetterie(self, row):
		print >>sys.stderr, "\nINFO : _insert_billetterie(self, row)"
		if not self.context['budgetsoiree']:
			try:
				self.context['budgetsoiree'] = BudgetSoiree.objects.get(soiree=self.context['soiree'])
			except BudgetSoiree.DoesNotExist as e:
				logging.error('[{}] Erreur       : {}'.format(self.database.line_num, e))
				self.report['error']+=1
				return None
		
		if (row['be_parterre'] or row['bf_recette_parterre']):
			if (row['be_parterre'].strip() == ''):
				self.__insert_billet(row['be_parterre'].strip(), self._tov(row['bf_recette_parterre'].strip()), '0')				
			else:
				be_parterre = row['be_parterre'].strip()
				be_parterre_split = re.split(',',be_parterre)
				self.__insert_billet(be_parterre_split[0], self._tov(row['bf_recette_parterre'].strip()), '0')
		if (row['ay_premiere'] or row['az_recette_premiere']):
			self.__insert_billet(row['ay_premiere'].strip(), self._tov(row['az_recette_premiere'].strip()), '1')
		if (row['au_balcon_premiere'] or row['av_recette_balcon_premiere']):
			rem, nbre = '', 0
			if row['au_balcon_premiere']:
				remarque = row['au_balcon_premiere'].replace('_', ' ').strip()
				mobj = re.match('(\d+)\s*\((\.+)\)', remarque)
				if mobj:
					nbre = mobj.group(0)
					rem = mobj.group(1)					
			self.__insert_billet(nbre, self._tov(row['av_recette_balcon_premiere'].strip()), '2', 'billets', rem)
		if (row['ba_deuxieme'] or row['bb_recette_deuxieme']):
			self.__insert_billet(row['ba_deuxieme'].strip(), self._tov(row['bb_recette_deuxieme'].strip()), '3')
		if (row['aw_balcon_deuxieme'] or row['ax_recette_balcon_deuxieme']):
			self.__insert_billet(row['aw_balcon_deuxieme'].strip(), self._tov(row['ax_recette_balcon_deuxieme'].strip()), '4')
		if ((row['bc_troisieme'] or row['bd_recette_troisieme']) and row['bc_troisieme'] != '_'): 
			if (row['bc_troisieme'].strip() == ''):
				self.__insert_billet(row['bc_troisieme'].strip(), self._tov(row['bd_recette_troisieme'].strip()), '5')				
			else:
				bc_troisieme = row['bc_troisieme'].strip()
				bc_troisieme_split = re.split(',',bc_troisieme)
				self.__insert_billet(bc_troisieme_split[0], self._tov(row['bd_recette_troisieme'].strip()), '5')
			
		if (row['bo_paradis'] or row['bp_recette_paradis']):
			self.__insert_billet(row['bo_paradis'].strip(), self._tov(row['bp_recette_paradis'].strip()), '6')
		if (row['bm_supplement'] or row['bn_recette_supplement']):
			rem = ''
			if row['bm_supplement']:
				remarque = row['bm_supplement'].replace('_', ' ').strip()
				mobj = re.match('[Oo]ui\s*(\.+)', remarque)
				if mobj:
					rem = mobj.group()
			self.__insert_billet('', self._tov(row['bn_recette_supplement'].strip()), '7', 'billets', rem)
		if (row['bg_prima_loggia'] or row['bh_recette_prima_loggia']):
			self.__insert_billet(row['bg_prima_loggia'].strip(), self._tov(row['bh_recette_prima_loggia'].strip()), '8')
		if (row['bi_seconda_loggia'] or row['bj_recette_seconda_loggia']):
			self.__insert_billet(row['bi_seconda_loggia'].strip(), self._tov(row['bj_recette_seconda_loggia'].strip()), '9')
		if (row['bk_personnalite'] or row['bl_recette_personnalite']):
			pers = row['bk_personnalite'].replace('_', ' ').strip().split(';')
			if(row['bl_recette_personnalite']):
				val = row['bl_recette_personnalite'].strip().split(';')
			else:
				val = '0'
			for i in range(len(pers)):
				v=''
				if val[i]:
					v = self._tov(val[i])
				self.__insert_billet(len(pers), v, '10', 'billets' , pers[i]) # /!\ lib remplis pour le texte aille dans rem donc commentaire


	def __insert_billet(self, nbre, montant, type_b, lib='billets', rem=''):
		print >>sys.stderr, "	INFO : __insert_billet(self, "+str(nbre)+" , "+str(montant)+" , "+str(type_b)+" , "+str(lib)+" , "+str(rem)+")"
		rec = {}
		new_billet=None
		# /!\ ERREURS DU CSV POUR LE NOMBRE DE BILLETS VENDUS
		if (nbre=='' or nbre=='Ill.' or nbre=='__'):
			print >>sys.stderr, "		ERR : nbre=='Ill.'"
			rec['nombre_billets_vendus'] = -1
		elif isinstance(nbre, int):
			rec['nombre_billets_vendus'] = nbre
		else:
			rec['nombre_billets_vendus'] = int(float(nbre.replace(',','.')))

		rec['type_billet'] = type_b
		rec['montant'] = montant
		rec['libelle'] = lib
		rec['budget'] = self.context['budgetsoiree']
		rec['commentaire'] = rem
		form = BilletterieForm(rec)
		print >>sys.stderr, "		ERR: form billet "+str(form.errors)
		try:
			form.is_valid()
		except ValidationError as e:
			logging.error('[{}] Erreur       : {}'.format(self.database.line_num, e))
			self.report['error']+=1
		else:
			new_billet = form.save(commit=False)
			new_billet.montant = montant
			new_billet.budget = self.context['budgetsoiree']
			try:
				new_billet = form.save(commit=True)
			except ValueError as e:
				logging.error('[{}] Erreur       : {}'.format(self.database.line_num, e))
				self.report['error']+=1
			except (ValidationError, IntegrityError) as e: # la recette est déjà enregistrée !
				logging.error('[{}] Erreur       : {}'.format(self.database.line_num, e))
				self.report['error']+=1
		return new_billet
			

	def _insert_soiree(self, row):
		print >>sys.stderr, "\nINFO : _insert_soiree(self, row)"
		rec = {}
		new_soiree = None
		mois=0
		if not row['_h_mois']: pass
		elif row['_h_mois'].strip().lower() in ['1', 'gennaro', 'genaro', 'gienaro', 'gen°', 'gen¬_', 'janvier', 'jan']: mois=1
		elif row['_h_mois'].strip().lower() in ['2', 'febrario', 'febraro', 'febro', 'février', 'fevrier', 'feb']: mois=2
		elif row['_h_mois'].strip().lower() in ['3', 'marzo', 'mars', 'mar']: mois=3
		elif row['_h_mois'].strip().lower() in ['4', 'aprile', 'ape', 'avril', 'apr']: mois=4
		elif row['_h_mois'].strip().lower() in ['5', 'maggio', 'magg°', 'mag°','mag¬_', 'magg¬_', 'mai', 'may']: mois=5
		elif row['_h_mois'].strip().lower() in ['6', 'giugno', 'zugg°', 'zugg¬_', 'zug°', 'zug¬_', 'juin', 'jun']: mois=6
		elif row['_h_mois'].strip().lower() in ['7', 'luglio', 'lugg°', 'lug°', 'lugl°', 'lug¬_', 'lugg¬_', 'lugl¬_', 'juillet', 'jul']: mois=7
		elif row['_h_mois'].strip().lower() in ['8', 'agosto', 'agto', 'agt°', 'agt¬_', 'août', 'aout', 'aug']: mois=8
		elif row['_h_mois'].strip().lower() in ['9', 'settembre', 'setembre', '7bre', 'se', 'septembre', 'sep']: mois=9
		elif row['_h_mois'].strip().lower() in ['10', 'ottobre', 'otobre', 'ottombre', '8bre', 'otto', 'octobre', 'oct']: mois=10
		elif row['_h_mois'].strip().lower() in ['11', 'novembre', 'novbre', '9bre', 'nov']: mois=11
		elif row['_h_mois'].strip().lower() in ['12', 'decembre', 'xmbre', 'xbre', '10bre', 'dto', 'detto', 'décembre', 'dec']: mois=12
		else:
			logging.error('[{}] Erreur       : Le mois {!r} est inconnu'.format(self.database.line_num, row['_h_mois']))
			self.report['error']+=1

		print >>sys.stderr, "INFO: row['_g_num'] and mois!=0 and row['_i_annee']: "+str(row['_g_num'])+" "+str(mois)+" "+str(row['_i_annee'])
		if row['_g_num'] and mois!=0 and row['_i_annee']:
			rec['date']='{}-{}-{}'.format(row['_i_annee'].strip(), mois, row['_g_num'].strip())
			rec['libelle_date_reg'] = '{} {} {} {}'.format(
				row['_f_jour'].strip().capitalize(),
				row['_g_num'].strip(),
				row['_h_mois'].strip().capitalize(),
				row['_i_annee'].strip())
			rec['ligne_src'] = self.database.line_num
		
			soiree = None
			print >>sys.stderr, "INFO: rec['date'] "+rec['date']
			try:
				soiree = Soiree.objects.get(date=rec['date'])
				self.context['soiree'] = soiree
			except (ValueError, ValidationError) as e:
				logging.error('[{}] Erreur       : {}'.format(self.database.line_num, e))
				self.report['error']+=1
			except Soiree.DoesNotExist:
				print >>sys.stderr, "INFO: Soiree.DoesNotExist"
				form = SoireeForm(rec)
				try:
					form.is_valid()
				except ValidationError as e:
					logging.error('[{}] Erreur       : {}'.format(self.database.line_num, e))
					self.report['error']+=1
				else:				
					new_soiree = form.save(commit=False)	# commit lors de l'enregistrement du budget de la soirée 
					self.context['soiree'] = new_soiree
					print >>sys.stderr, "INFO : self.context['soiree'] "+str(self.context['soiree'])
					if self.context['soiree']:
						print >>sys.stderr, "INFO : NEW SOIREE 1 self.context['pageregistre']-> "+str(self.context['pageregistre'])
						
						self.context['soiree'].page_registre = self.context['pageregistre']
						
						if row['as_total_depenses_reg']:
							self.context['soiree'].budget = self.context['budgetsoiree']
							print>> sys.stderr, "INFO: self.context insere ['soiree'].budget "+str(self.context['soiree'].budget)
						else:
							print>> sys.stderr, "INFO: self.context non insere car NULL ['soiree'].budget "+str(self.context['soiree'].budget)
							
						print >>sys.stderr, "INFO : self.context['budgetsoiree'] "+str(self.context['budgetsoiree'])
						self.context['soiree'].save()	# commit pour l'enregistrement de la soirée

					else:
						
						logging.error('[{}] Erreur       : soirée inconnue !'.format(self.database.line_num))
						self.report['error']+=1

		else:	# pas de soirée sur la ligne
			pass
		return new_soiree

# duplicates raise django.db.utils.IntegrityError
		
	def _insert_pageregistre(self, row):
		print >>sys.stderr, "\nINFO : _insert_pageregistre(self, row)"
		rec = {}
		new_reg = None
		if row['_a_ref_registre'] and row['_b_num_page_pdf']:	# champs non vides
			ref_registre_test = row['_a_ref_registre'].strip().replace('_', '-').upper()
			if not self.context['pageregistre']:
				print >>sys.stderr, "INFO: NEW PAGE REGISTRE 1"
				rec['ref_registre']= row['_a_ref_registre'].strip().replace('_', '-').upper()
				rec['num_page_pdf']= row['_b_num_page_pdf'].strip()
			
				try:
					pr = PageRegistre.objects.get(**rec)
					self.context['pageregistre'] = pr
				except PageRegistre.DoesNotExist:
					form = PageRegistreForm(rec)
					if form.is_valid():
						new_reg= form.save()
						self.context['pageregistre'] = new_reg
					else:
						logging.error('[{}] Erreur       : {}'.format(self.database.line_num, form.errors))
						self.report['error']+=1	
			elif self.context['pageregistre'].ref_registre == ref_registre_test and str(self.context['pageregistre'].num_page_pdf) != str(row['_b_num_page_pdf']):
				print >>sys.stderr, "INFO: NEW PAGE REGISTRE 2 "+str(self.context['pageregistre'].ref_registre)+"->"+str(ref_registre_test)+" "+str(self.context['pageregistre'].num_page_pdf)+"->"+str(row['_b_num_page_pdf'])
				rec['ref_registre']= row['_a_ref_registre'].strip().replace('_', '-').upper()
				rec['num_page_pdf']= row['_b_num_page_pdf'].strip()
			
				try:
					pr = PageRegistre.objects.get(**rec)
					self.context['pageregistre'] = pr
				except PageRegistre.DoesNotExist:
					form = PageRegistreForm(rec)
					if form.is_valid():
						new_reg= form.save()
						self.context['pageregistre'] = new_reg
					else:
						logging.error('[{}] Erreur       : {}'.format(self.database.line_num, form.errors))
						self.report['error']+=1	
			elif self.context['pageregistre'].ref_registre != ref_registre_test and self.context['pageregistre'].num_page_pdf != row['_b_num_page_pdf']:
				print >>sys.stderr, "INFO: NEW PAGE REGISTRE 3 "+str(self.context['pageregistre'].ref_registre)+"->"+str(row['_a_ref_registre'])+" "+str(self.context['pageregistre'].num_page_pdf)+"->"+str(row['_b_num_page_pdf'])
				rec['ref_registre']= row['_a_ref_registre'].strip().replace('_', '-').upper()
				rec['num_page_pdf']= row['_b_num_page_pdf'].strip()
			
				try:
					pr = PageRegistre.objects.get(**rec)
					self.context['pageregistre'] = pr
				except PageRegistre.DoesNotExist:
					form = PageRegistreForm(rec)
					if form.is_valid():
						new_reg= form.save()
						self.context['pageregistre'] = new_reg
					else:
						logging.error('[{}] Erreur       : {}'.format(self.database.line_num, form.errors))
						self.report['error']+=1	
			else:
				pass		
		else:	# pas de page de registre sur la ligne
			pass
		return new_reg

def list (request):
	logging.basicConfig(
		filename=os.path.join(regital.settings.MEDIA_ROOT,'out.log'),
		filemode='w',
		format='%(asctime)s - %(levelname)s: %(message)s',
		datefmt='%m/%d/%Y %I:%M:%S %p',
		level=logging.INFO)
	logging.info('Initializing db...')
	parser=CSVParser()
	logging.info('Populating db...')
	parser.bulk_insert()
	return render_to_response(
		'upload2.html',
		{'info': parser.info},
		context_instance=RequestContext(request)
	)