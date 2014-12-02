#-*- coding: utf-8 -*-
from navigation.models import *
from django import forms
from django.forms.models import modelform_factory

# définition de tous les formulaires associés au modèle (un par classe)

PersonneForm = modelform_factory( Personne, 
	fields=[
		'nom','prenom','pseudonyme','genre','nationalite','titre_personne','date_de_naissance','date_de_deces','uri_cesar',
		'plus_dinfo','date_de_deces_text','date_de_deces_isComplete','date_de_naissance_text','date_de_naissance_isComplete'],
	widgets={
    'nom': forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Nom', 'onblur' :'recupPersonneInfo()'}),
    'prenom': forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Prénom'}),
    'pseudonyme': forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Pseudonyme'}),
    'genre': forms.RadioSelect(attrs={'class' : 'radio inline'}),
    'nationalite': forms.Select(attrs={'class' : 'form-control'}),
    'titre_personne': forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Titre', 'name' : 'titre_personne'}),
    'date_de_naissance': forms.TextInput(attrs={'class' : 'form-control', 'value':'1700-01-01', 'id' : 'dpersonne1' }),
		'date_de_deces': forms.TextInput(attrs={'class' : 'form-control', 'value':'1700-01-01', 'id' : 'dpersonne2'}),
		'uri_cesar': forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Uri Cesar'}),
    'plus_dinfo': forms.Textarea(attrs={'class' : 'form-control', 'placeholder' : '...'}),
		'date_de_deces_text': forms.HiddenInput(attrs={'value':''}),
		'date_de_deces_isComplete': forms.HiddenInput(attrs={'value':'True'}),
		'date_de_naissance_text': forms.HiddenInput(attrs={'value':''}),
		'date_de_naissance_isComplete': forms.HiddenInput(attrs={'value':'True'}), 
    },
  labels={
    'prenom': 'Prénom',
    'date_de_deces': 'Décès',
    'date_de_naissance': 'Naissance',
		'date_de_naissance_text': '',
		'date_de_naissance_isComplete': '',
		'date_de_deces_text': '',
		'date_de_deces_isComplete': '',
  })
    
PieceForm = modelform_factory( Piece,
	fields=[
		'titre','titre_brenner','date_premiere','langue','auteurs','uri_theaville','commentaire','date_premiere_text','date_premiere_isComplete'
	],
	widgets={
    'titre': forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Titre', 'onblur' :'recupPieceInfo()'}),
    'titre_brenner': forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Titre Brenner'}),
    'uri_theaville': forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Uri Theaville'}),
    'date_premiere': forms.TextInput(attrs={'class' : 'form-control', 'value':'1700-01-01', 'id' : 'dpiece1' }),
		'date_premiere_text': forms.HiddenInput(attrs={'value':''}),
		'date_premiere_isComplete': forms.HiddenInput(attrs={'value':'True'}),
    'langue': forms.Select(attrs={'class' : 'form-control'}),
    'auteurs': forms.SelectMultiple(attrs={'class' : 'form-control'}),
    'commentaire': forms.Textarea(attrs={'class' : 'form-control', 'placeholder' : '...'})
    },
  labels={
    'date_premiere': 'Première',
    'titre_brenner': 'Titre Brenner',
    'uri_theaville': 'Uri Theaville',
		'date_premiere_text': '',
		'date_premiere_isComplete': ''
  })   
    
SoireeForm = modelform_factory( Soiree,
  fields=('date', 'libelle_date_reg'),
	widgets={
		'date': forms.TextInput(attrs={'class' : 'form-control', 'value':'1700-01-01', 'id' : 'dsoiree1' }),
		'libelle_date_reg': forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Date tel qu\'elle est dans le registre'}),
	},
  labels={
    'libelle_date_reg': 'Date Registre'
  }
)

BudgetSoireeFormInputs = modelform_factory( BudgetSoiree,
  fields=['credit_final_reg', 'debit_initial_reg','montant_cachet','montant_cachet_auteur','nb_total_billets_vendus_reg','nombre_cachets','quart_pauvre_reg','reste_reg','total_depenses_reg','total_recettes_reg','debit_derniere_soiree_reg','total_depenses_corrige_reg'],
  widgets={
    'credit_final_reg': forms.NumberInput(),
    'debit_initial_reg': forms.NumberInput(),
    'montant_cachet': forms.NumberInput(),
    'montant_cachet_auteur': forms.NumberInput(),
    'nb_total_billets_vendus_reg': forms.NumberInput(),
    'nombre_cachets': forms.NumberInput(),
    'quart_pauvre_reg': forms.NumberInput(),
    'reste_reg': forms.NumberInput(),
    'total_depenses_reg': forms.NumberInput(),
    'total_recettes_reg': forms.NumberInput(),
    'debit_derniere_soiree_reg': forms.NumberInput(),
    'total_depenses_corrige_reg': forms.NumberInput(),
  },
  labels={
    'credit_final_reg':'Crédit Final', 
    'debit_initial_reg':'Débit Initial',
    'montant_cachet':'Montant Cachet',
    'montant_cachet_auteur':'Montant Cachet Auteur',
    'nb_total_billets_vendus_reg':'Total Billets Vendus',
    'nombre_cachets':'Nombre Cachets',
    'quart_pauvre_reg':'Quart Pauvre',
    'reste_reg':'Reste',
    'total_depenses_reg': 'Total Dépenses',
    'total_recettes_reg': 'Total Recettes',
    'debit_derniere_soiree_reg': 'Débit dernière soirée',
    'total_depenses_corrige_reg': 'Dépenses corrigées',
  }
)

BudgetSoireeForm = modelform_factory( BudgetSoiree,
  fields=['credit_final_reg', 'debit_initial_reg','montant_cachet','montant_cachet_auteur','nb_total_billets_vendus_reg','nombre_cachets','quart_pauvre_reg','reste_reg','total_depenses_reg','total_recettes_reg','debit_derniere_soiree_reg','total_depenses_corrige_reg'],
	widgets={
		'credit_final_reg': forms.TextInput(attrs={'class' : 'form-control input-sm', 'placeholder' : 'Crédit final'}),
		'debit_initial_reg': forms.TextInput(attrs={'class' : 'form-control input-sm', 'placeholder' : 'Débit initial'}),
		'montant_cachet': forms.Select(attrs={'class' : 'form-control input-sm'}),
		'montant_cachet_auteur': forms.TextInput(attrs={'class' : 'form-control input-sm', 'placeholder' : 'Montant cachet de l\'auteur'}),
		'nb_total_billets_vendus_reg': forms.NumberInput(attrs={'class' : 'form-control input-sm', 'placeholder' : 'Nombre total de billets vendus'}),
		'nombre_cachets': forms.TextInput(attrs={'class' : 'form-control input-sm', 'placeholder' : 'Nombre de cachets'}),
		'quart_pauvre_reg': forms.TextInput(attrs={'class' : 'form-control input-sm', 'placeholder' : 'Quart du pauvre'}),
		'reste_reg': forms.TextInput(attrs={'class' : 'form-control input-sm', 'placeholder' : 'Reste'}),
		'total_depenses_reg': forms.TextInput(attrs={'class' : 'form-control input-sm', 'placeholder' : 'Total dépenses'}),
		'total_recettes_reg': forms.TextInput(attrs={'class' : 'form-control input-sm', 'placeholder' : 'Total recettes'}),
		'debit_derniere_soiree_reg': forms.TextInput(attrs={'class' : 'form-control input-sm', 'placeholder' : 'Débit dernière soirée'}),
		'total_depenses_corrige_reg': forms.TextInput(attrs={'class' : 'form-control input-sm', 'placeholder' : 'Dépenses corrigées'}),
	},
	labels={
    'credit_final_reg':'Crédit Final', 
    'debit_initial_reg':'Débit Initial',
    'montant_cachet':'Montant Cachet',
    'montant_cachet_auteur':'Montant Cachet Auteur',
    'nb_total_billets_vendus_reg':'Total Billets Vendus',
    'nombre_cachets':'Nombre Cachets',
    'quart_pauvre_reg':'Quart Pauvre',
    'reste_reg':'Reste',
		'total_depenses_reg': 'Total Dépenses',
		'total_recettes_reg': 'Total Recettes',
		'montant_cachet': 'Cachet',
		'montant_cachet_auteur': 'Cachet Auteur',
		'debit_derniere_soiree_reg': 'Débit dernière soirée',
		'total_depenses_corrige_reg': 'Dépenses corrigées',
	}
)  

PageRegistreForm = modelform_factory(PageRegistre,
  fields=('ref_registre','num_page_pdf','redacteurs'),
  widgets={
    'ref_registre' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Référence Registre'}),
    'num_page_pdf' : forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : 'Numéro page du PDF'}),
		'redacteurs' : forms.SelectMultiple(attrs={'class' : 'form-control'}),
  },
  labels={
    'ref_registre':'Référence Registre',
    'num_page_pdf':'Numéro page PDF',
  }
)

DebitFormInputs = modelform_factory(Debit,
  fields=('type_depense','libelle','montant','traduction','mots_clefs'),
  widgets={
    'montant': forms.NumberInput(),
    'libelle' : forms.TextInput(),
    'type_depense' : forms.NumberInput(),
    'traduction' : forms.TextInput(),
    'mots_clefs' : forms.TextInput(),
  },
  labels={
    'montant':'',
    'libelle':'',
    'type_depense':'Type de dépense',
    'traduction':'',
    'mots_clefs':'',
  }
)

DebitForm = modelform_factory(Debit,
  fields=('type_depense','libelle','montant','traduction','mots_clefs'),
  widgets={
    'montant': forms.TextInput(attrs={'class' : 'form-control input-sm', 'placeholder' : 'Montant'}),
    'libelle' : forms.TextInput(attrs={'class' : 'form-control input-sm', 'placeholder' : 'Libellé'}),
    'type_depense' : forms.Select(attrs={'class' : 'form-control input-sm'}),
    'traduction' : forms.TextInput(attrs={'class' : 'form-control input-sm', 'placeholder' : 'Traduction'}),
    'mots_clefs' : forms.TextInput(attrs={'class' : 'form-control input-sm', 'placeholder' : 'Mots clefs'}),
  },
  labels={
    'montant':'',
    'libelle':'',
    'type_depense':'Type de dépense',
    'traduction':'',
    'mots_clefs':'',
  }
)

CreditForm = modelform_factory(Credit,
  fields=('libelle','montant'),
  widgets={
		'libelle' : forms.TextInput(attrs={'class' : 'form-control input-sm', 'placeholder' : 'Libellé'}),
    'montant': forms.TextInput(attrs={'class' : 'form-control input-sm', 'placeholder' : 'Montant'}),
  },
  labels={
    'montant':'',
    'libelle':'',
  }
)

BilletterieForm = modelform_factory(Billetterie,
  fields=('montant','libelle','nombre_billets_vendus','type_billet','commentaire'),
  widgets={
    'montant': forms.TextInput(attrs={'class' : 'form-control input-sm', 'placeholder' : 'Montant'}),
    'libelle' : forms.TextInput(attrs={'class' : 'form-control input-sm', 'placeholder' : 'Libellé'}),
    'nombre_billets_vendus' : forms.TextInput(attrs={'class' : 'form-control input-sm', 'placeholder' : 'Nombre de billets vendus'}),
    'type_billet' : forms.Select(attrs={'class' : 'form-control input-sm'}),
    'commentaire' : forms.Textarea(attrs={'class' : 'form-control input-sm', 'placeholder' : 'Commentaire', 'rows':'1'}),
  },
  labels={
    'montant':'',
    'libelle':'',
    'nombre_billets_vendus':'',
    'type_billet':'Type billet',
    'commentaire':'',
  }
)

RepresentationFormInputs = modelform_factory(Representation,
  fields=('position','piece','Soiree'),
  widgets={
    'position': forms.NumberInput(),
    'piece' : forms.Select(),
    'Soiree' : forms.Select(),
  },
  labels={
  }
)

RepresentationForm = modelform_factory(Representation,
  fields=('position','piece'),
  widgets={
    'position': forms.NumberInput(attrs={'class' : 'form-control input-sm', 'placeholder' : 'Position'}),
    'piece' : forms.Select(attrs={'class' : 'form-control input-sm'}),
  },
  labels={
  }
)
AnimationForm = modelform_factory(Animation,
  fields=('position','type','auteur','description'),
  widgets={
    'position': forms.NumberInput(attrs={'class' : 'form-control input-sm', 'placeholder' : 'Position'}),
    'type' : forms.Select(attrs={'class' : 'form-control input-sm'}),
    'auteur' : forms.Select(attrs={'class' : 'form-control input-sm'}),
    'description' : forms.Textarea(attrs={'class' : 'form-control input-sm', 'placeholder' : 'Description', 'rows':'1'}),
  },
  labels={
  }
)
RoleForm = modelform_factory(Role,
  fields=('personne','representation','role','plus_dinfo'),
  widgets={
    'personne': forms.Select(attrs={'class' : 'form-control input-sm'}),
    'representation' : forms.Select(attrs={'class' : 'form-control input-sm', 'onclick' : 'updateRepresentationSelect(this)'}),
    'role' : forms.TextInput(attrs={'class' : 'form-control input-sm', 'placeholder' : 'Rôle'}),
    'plus_dinfo' : forms.Textarea(attrs={'class' : 'form-control input-sm', 'placeholder' : 'Information supplémentaire', 'rows':'1'}),
  },
  labels={
  }
)

TransactionSoireeForm = modelform_factory(TransactionSoiree)
TransactionAbonnementForm = modelform_factory(TransactionAbonnement)
AbonnementForm = modelform_factory(Abonnement)
RecapitulatifForm = modelform_factory(Recapitulatif)
DebitRecapitulatifForm = modelform_factory(DebitRecapitulatif)
CreditRecapitulatifForm = modelform_factory(CreditRecapitulatif)