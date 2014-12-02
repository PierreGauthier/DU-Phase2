
 #-*- coding: utf-8 -*-

from django import template

register = template.Library()

@register.filter(name='div')
def div(value,arg):
	return value/arg

@register.filter(name='mult')
def mult(value,arg):
	return value*arg	