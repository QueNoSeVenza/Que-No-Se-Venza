# -*- coding: utf-8 -*-
from datetime import datetime
from .models import *
from django.core import mail

#Esta funcion devuelve una lista de entidades que comparten campo medicamento con la entidad
#que se use como argumento, si esta ultima es un MeicamentoDonado la lista contendra Peticiones
#y si es una Peticion contendra MedicamentosDonados.  

def getMatches(entity):

	if entity.__class__.__name__ == "Pedido":

		not_dull_medicines = [medicamento.id for medicamento in MedicamentoDonado.objects.all() if medicamento.isDull() == False]
		return MedicamentoDonado.objects.filter(medicamento=entity.medicamento, id__in=not_dull_medicines).order_by('fecha_vencimiento')
	
	elif entity.__class__.__name__ == "MedicamentoDonado":

		return MedicamentoDonado.objects.filter(medicamento=entity.medicamento)

#Esta funcion resta la cantidad del pedido a uno o varios MedicamentoDonado
#y guarda los cambios en la base de datos. Requiere que se le pase un Pedido.

def executeMatch(petition):

	match_list = getMatches(petition)
	
	for match in match_list:
		match.cantidad -= petition.cantidad
		if match.cantidad >= 0:

			match.save()
			return True

		else: 

			petition.cantidad = abs(match.cantidad)
			match.cantidad = 0
			match.save()
			
	return False


#Devuelve una lista de los medicamentos vencidos.

def getDullMedicines():
	
	dull_medicines = [medicamento.id for medicamento in MedicamentoDonado.objects.all() if medicamento.isDull() == False]
	return MedicamentoDonado.objects.filter(id__in=dull_medicines)

	
