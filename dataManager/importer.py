# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from dataManager.models import *
from django.db import IntegrityError
import yaml

class Importer:
	def __init__(self):
		self.data = []
	def importYaml(self, yamlfile):
		yamlInfo = {}
	
		for yamlInfo in yaml.load_all(file(yamlfile, 'r')):
			self._import(self._cleanYaml(yamlInfo))
			# return yamlInfo 
			
	def _import(self, yamlData, key = None, parentKey = None, parentInstance = None):
		
		if isinstance(yamlData, dict):
			
			instance = None
			
			if key != None:
				
				non_object_attributes = (x for x in yamlData.iterkeys() if not isinstance(yamlData[x], (dict, list)))
				object_attributes = (x for x in yamlData.iterkeys() if isinstance(yamlData[x], (dict, list)))
				attributesList = []
				exec "attributesList = dir(self._to_class_name(key))" in globals(), locals()
								
				first_part_cmd = "instance = " + self._to_class_name(key) + "("
				if parentKey != None and parentKey in attributesList :
					first_part_cmd += "parentKey = parentInstance,"
				for attribute in non_object_attributes :
					first_part_cmd += attribute +" = self._import(yamlData[\'"+attribute+"\'], \'"+attribute+"\'),"
				first_part_cmd += ")\ninstance.save()"
				first_part_cmd = first_part_cmd.replace(",)", ")")
				
				try:
					exec first_part_cmd in globals(), locals()
				except IntegrityError:
					print key + " already exist"
						
				for attribute in object_attributes :
					print key
					attributeValue = self._import(yamlData[attribute], attribute, key, instance)
					if hasattr(instance, attribute):
						setattr(instance, attribute, attributeValue);
			
			else :
				for attribute in yamlData.iterkeys():
					instance = self._import(yamlData[attribute], attribute)
			
			return instance
			
		if isinstance(yamlData, list):
			return [self._import(element, key) for element in yamlData]
		
		return yamlData
		
	def _cleanYaml(self, yamlData):
		keysList = [key for key in yamlData.iterkeys()]		
		for key in keysList:
			newKey = self._to_attribute_name(key)
			if isinstance(yamlData[key], dict):
				yamlData[newKey] = self._cleanYaml(yamlData[key])	
			elif isinstance(yamlData[key], list):
				newList = [self._cleanYaml(el) for el in yamlData[key] if isinstance(el, dict)]	
				newList.append(el for el in yamlData[key] if not isinstance(el, dict))
				yamlData[newKey] = newList
			else:
				yamlData[newKey] = yamlData[key]	
			if key != newKey : del yamlData[key]
		return yamlData
						
	def _to_class_name(self, value):		
		classname = ""
		
		for x in value.split(" ") :
			classname = classname + x.capitalize()

		classname = classname.replace('é', 'e')
		
		if classname == "Budget":
			return "BudgetSoiree"
		elif classname == "Depenses":
			return "Depense"
			
		return classname
	
	def _to_attribute_name(self, value):
		attributename = "_"
		
		for x in value.split(" ") :
			attributename = attributename + "_" + x
		
		attributename = attributename.replace('__', '')
		attributename = attributename.replace('è', 'e')
		attributename = attributename.replace('é', 'e')
		
		return attributename.replace('é', 'e')
		