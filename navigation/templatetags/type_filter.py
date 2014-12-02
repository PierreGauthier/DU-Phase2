
 #-*- coding: utf-8 -*-

from django import template
import datetime

register = template.Library()

@register.filter(name='type', is_safe=True)
def type_var(value):
	if type(value) is str : return 'str'
	elif type(value) is unicode : return 'unicode'
	elif type(value) is datetime.date :	return 'date'
	elif type(value) is list : return 'list'
	elif type(value) is dict : return 'dict'
	elif type(value) is int : return 'int'
	elif type(value) is float : return 'float'
	elif type(value) is bool : return 'bool'
	else : return 'unknow'
	