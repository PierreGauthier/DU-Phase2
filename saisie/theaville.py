#-*- coding: utf-8 -*-
 
import re
import requests
from django.shortcuts import get_object_or_404, render, render_to_response
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponse		 
 
def searchPiece(request, titre='', auteur=''):				
	payload = {'r': 'pieces', 'titre': titre, 'auteur': auteur,'crea_de_annee':'1709','crea_a_annee':'1794',
						'rep_de_annee':'1709', 'rep_a_annee':'1794'}

	r = requests.get("http://www.theaville.org/kitesite/index.php", params=payload,	 
					 proxies= 
					 {
						 "http": "http://cache.wifi.univ-nantes.fr:3128",
						 "https": "http://cache.wifi.univ-nantes.fr:3128",
					 }
	)
	page = r.text
#	page = getPage1()

	page = page[page.index("<!--   Document   -->"):page.index('<br class="nettoyeur" />')]
	if not u'0 r&eacute;sultat&nbsp;:' in page :	 
		page = page[page.index("<table"):page.index("</table>")+8]
		page = '<div style="overflow:auto; height:30em;"><table class="table table-striped">' + page[page.index("</thead>")+8:] + '</div>'

		pattern = '(\r|\t|(  )|(<em>)|(</em>)|\')*'
		pattern = re.compile(pattern, re.UNICODE)
		page = pattern.sub(r'',page)
		
		pattern = '<a href="index.php.r=pieces/auteurs/details.php&amp;id=(?P<id>\d+)">'
		pattern = re.compile(pattern, re.UNICODE | re.DOTALL)
		page = pattern.sub(r' ',page)
		
		page = page.replace(u'<br />\n', u'')
		
		pattern = '''<tr>
<td><a href="index.php.r=pieces/afficher&amp;id=(?P<id>\d+)">(?P<titre>.+)</a></td>
<td>.+</td>
<td>(?P<annee>\d+)</td>
<td>(?P<auteurs>.*)</td>
</tr>\n'''
		pattern = re.compile(pattern, re.UNICODE)
		page = pattern.sub(r'''<tr style="cursor:pointer;" onclick="parsePieceInfo(\g<id>,'\g<titre>','\g<auteurs>','\g<annee>')">
<td><span class="glyphicon glyphicon-book"></span></td>
<td>\g<titre><td/>
<td>\g<annee><td/>
<td>\g<auteurs><td/></tr>''',page)
		
		return HttpResponse(page, content_type="text/plain")
	else:
		return HttpResponse('Aucune Piece ne correspond', content_type="text/plain")
		
def getInfoPiece(request, id):
	payload = {'fct': 'edit', 'person_UOID': id }
	r = requests.get("http://www.cesar.org.uk/cesar2/people/people.php", params=payload 
		# ,proxies= 
		# {
			# "http": "http://cache.wifi.univ-nantes.fr:3128",
			# "https": "http://cache.wifi.univ-nantes.fr:3128",
		# }
	)
	page = r.text
#	page = getPage2()

	page = page[page.index("<H1>People</H1>"):page.index("<H2>Notes</H2>")] 
	infos = ''

	for i in range(1,10):
		page = page[page.index('keyColumn')+1:]
		if i == 8 :
			infos = infos + ';' + page[page.index('valueColumn')+19:page.index('keyColumn')-23]
		elif (i == 7) or (i == 6) : #si c'est une date
			infos = infos + ';' + page[page.index('valueColumn')+19:page.index('keyColumn')-29]
		else:
			infos = infos + ';' + page[page.index('valueColumn')+19:page.index('keyColumn')-29]

	return HttpResponse(infos, content_type="text/plain")		

def getPage1() :
	return u''' 

<!--   Document   -->


<small>Liste | <a href="index.php?r=pieces/cibles">Cibles</a> | <a href="index.php?r=pieces/lieux">Lieux</a> | <a href="index.php?r=pieces/auteurs">Auteurs&nbsp;</a></small><br /><br />

<h1 class="invisible">Liste des pi&egrave;ces</h1>

<p></p><strong>12 r&eacute;sultats&nbsp;:</strong></p>
<table id="table" class="pieces">
<thead>
  <tr>
    <th>Titre&nbsp;</th>
    <th>Parodie de&nbsp;</th>
    <th>Cr&eacute;ation&nbsp;</th>
    <th>Auteur(s)&nbsp;</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td><a href="index.php?r=pieces/afficher&amp;id=11">Arlequin Amadis</a></td>
    <td><em>Amadis de Gaule</em> de Quinault et Lully</td>
    <td>1731</td>
    <td><a href="index.php?r=pieces/auteurs/details.php&amp;id=10">Biancolelli (Pierre-François) dit Dominique<br />
<a href="index.php?r=pieces/auteurs/details.php&amp;id=77">Romagnesi (Jean-Antoine)</td>
  </tr>
  <tr>
    <td><a href="index.php?r=pieces/afficher&amp;id=12">Arlequin Atys</a></td>
    <td><em>Atys</em> de Quinault et Lully</td>
    <td>1726</td>
    <td><a href="index.php?r=pieces/auteurs/details.php&amp;id=11">Boizard de Pontau (Claude Florimond)</td>
  </tr>
  <tr>
    <td><a href="index.php?r=pieces/afficher&amp;id=237">Arlequin Atys</a></td>
    <td><em>Atys</em> de Quinault et Lully</td>
    <td>1710</td>
    <td><a href="index.php?r=pieces/auteurs/details.php&amp;id=10">Biancolelli (Pierre-François) dit Dominique</td>
  </tr>
  <tr>
    <td><a href="index.php?r=pieces/afficher&amp;id=13">Arlequin Bellérophon</a></td>
    <td><em>Bellérophon</em> de T. Corneille/Fontenelle et Lully</td>
    <td>1728</td>
    <td><a href="index.php?r=pieces/auteurs/details.php&amp;id=10">Biancolelli (Pierre-François) dit Dominique<br />
<a href="index.php?r=pieces/auteurs/details.php&amp;id=77">Romagnesi (Jean-Antoine)</td>
  </tr>
  <tr>
    <td><a href="index.php?r=pieces/afficher&amp;id=17">Arlequin Marchand de poupées ou le Pygmalion moderne</a></td>
    <td><em>Pygmalion</em> de Rousseau et Coignet</td>
    <td>1779</td>
    <td><a href="index.php?r=pieces/auteurs/details.php&amp;id=30">Guillemain (Charles-Jacob)</td>
  </tr>
  <tr>
    <td><a href="index.php?r=pieces/afficher&amp;id=18">Arlequin Persée</a></td>
    <td><em>Persée</em> de Quinault et Lully</td>
    <td>1747</td>
    <td><a href="index.php?r=pieces/auteurs/details.php&amp;id=86">Valois d'Orville (de) (Adrien-Joseph)</td>
  </tr>
  <tr>
    <td><a href="index.php?r=pieces/afficher&amp;id=19">Arlequin Phaéton</a></td>
    <td><em>Phaéton</em> de Quinault et Lully</td>
    <td>1731</td>
    <td><a href="index.php?r=pieces/auteurs/details.php&amp;id=10">Biancolelli (Pierre-François) dit Dominique<br />
<a href="index.php?r=pieces/auteurs/details.php&amp;id=77">Romagnesi (Jean-Antoine)</td>
  </tr>
  <tr>
    <td><a href="index.php?r=pieces/afficher&amp;id=20">Arlequin Roland</a></td>
    <td><em>Roland</em> de Quinault et Lully</td>
    <td>1727</td>
    <td><a href="index.php?r=pieces/auteurs/details.php&amp;id=10">Biancolelli (Pierre-François) dit Dominique</td>
  </tr>
  <tr>
    <td><a href="index.php?r=pieces/afficher&amp;id=21">Arlequin Tancrède</a></td>
    <td><em>Tancrède</em> de Danchet et Campra</td>
    <td>1729</td>
    <td><a href="index.php?r=pieces/auteurs/details.php&amp;id=10">Biancolelli (Pierre-François) dit Dominique<br />
<a href="index.php?r=pieces/auteurs/details.php&amp;id=77">Romagnesi (Jean-Antoine)</td>
  </tr>
  <tr>
    <td><a href="index.php?r=pieces/afficher&amp;id=22">Arlequin Thésée</a></td>
    <td><em>Thésée</em> de Quinault et Lully</td>
    <td>1745</td>
    <td><a href="index.php?r=pieces/auteurs/details.php&amp;id=86">Valois d'Orville (de) (Adrien-Joseph)</td>
  </tr>
  <tr>
    <td><a href="index.php?r=pieces/afficher&amp;id=23">Arlequin Thétis</a></td>
    <td><em>Thétis et Pélée</em> de Fontenelle et Colasse</td>
    <td>1713</td>
    <td><a href="index.php?r=pieces/auteurs/details.php&amp;id=41">Le Sage (Alain-René)</td>
  </tr>
  <tr>
    <td><a href="index.php?r=pieces/afficher&amp;id=115">Le Mariage d'Arlequin et de Silvia, ou Thétis et Pélée déguisés</a></td>
    <td><em>Thétis et Pélée</em> de Fontenelle et Colasse</td>
    <td>1724</td>
    <td><a href="index.php?r=pieces/auteurs/details.php&amp;id=10">Biancolelli (Pierre-François) dit Dominique</td>
  </tr>
</tbody>
</table>
<br />

<script>
$(document).ready(function(){
  $('#table').dataTable({

    "iDisplayLength": 25,
    "aLengthMenu": [[10, 25, 50, 100], [10, 25, 50, 100]],
    "oLanguage": {
		"sLengthMenu": "Afficher _MENU_ lignes",
		"sSearch": "Recherche&nbsp;:",
		"oPaginate": {
			"sNext": "suivant",
			"sPrevious": "pr&eacute;c&eacute;dent"
		}
    }
  });
});
</script>

<br class="nettoyeur" />
	'''

