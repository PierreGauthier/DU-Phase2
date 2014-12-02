
 #-*- coding: utf-8 -*-

from django import template
from navigation.currency import *

register = template.Library()

@register.filter(name='currency', is_safe=True)
def currency(value):
	if value == '':
		return ''
	else:
		return numberToCurrency(int(value))
	