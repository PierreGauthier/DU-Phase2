
 #-*- coding: utf-8 -*-

from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag(takes_context = True)
def generate_arianne(context, title):
		
	session = context['request'].session
	
	current_url = context['request'].get_full_path()

	if 'arianne' not in session :
		session['arianne'] = title + ':/;'
		session['prevTitle'] = title

	if title =='Accueil' :
		session['arianne'] = title + ':/;'
		session['prevTitle'] = title

	arianne = ''
	arianneLine = session['arianne'].split(';')
	session['arianne'] = ''
	
	for el in arianneLine :
		if el != '' :
			session['arianne'] += el + ':' + current_url + ';'
			item = el.split(':')
			name = item[0]
			url = item[1]
			if name != title :
				arianne += '<li><a href="'+url+'">'+name+'</a></li>'
				if name == session['prevTitle'] :
					session['arianne'] += title + ':' + current_url + ';'
					arianne += '<li class="active">'+title+'</li>'
					session['prevTitle'] = title
					break
			else :
				arianne += '<li class="active">'+name+'</li>'
				session['prevTitle'] = title
				title = ''	# Pour pas qu'il ne soit réécrit à la fin du fil d'arianne
	
	context['request'].session = session

	return arianne
			