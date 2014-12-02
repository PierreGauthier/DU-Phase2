



class CurrencyError(Exception):
	def __init__(self):
		self.value = 0

# Change une chaine de caractere de la forme 12,25,54 (livre, sou, denier) une un entier (la valeur en denier)
def currencyToNumber(strValue):
	listValue = strValue.split(',')
	if len(listValue) == 3 :
		return (int(listValue[0])*240)+(int(listValue[1])*12)+int(listValue[2])
	elif len(listValue) == 2 :
		return (int(listValue[0])*240)+(int(listValue[1])*12)
	elif len(listValue) == 1 :
		return (int(listValue[0])*240)
	else:
		raise CurrencyError()
		
def numberToCurrency(intValue):
	livreValue = intValue/240
	souValue = (intValue - (livreValue*240))/12
	denierValue = intValue - (livreValue*240) - (souValue*12)
	return str(livreValue)+','+str(souValue)+','+str(denierValue)