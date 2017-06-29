# -*- coding: utf-8 -*-
from datetime import datetime
from .models import *
from django.core import mail
from django.core.mail import EmailMessage

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
#y guarda los cambios en la base de datos. Requiere que se le pase un Pedido y devuelve 
#una lista de (MedicamentoDonado,cantidad).

def executeMatch(petition):

	substaction_values = []
	match_list = getMatches(petition)
	


	for match in match_list:
		match.cantidad -= petition.cantidad
		if match.cantidad >= 0:
			substaction_values.append((match,petition.cantidad))
			match.save()
			return substaction_values

		else: 

			substaction_values.append((match,petition.cantidad-abs(match.cantidad)))
			petition.cantidad = abs(match.cantidad)

			match.cantidad = 0
			match.save()

	return substaction_values


#Devuelve una lista de los medicamentos vencidos.

def getDullMedicines():
	
	dull_medicines = [medicamento.id for medicamento in MedicamentoDonado.objects.all() if medicamento.isDull() == False]
	return MedicamentoDonado.objects.filter(id__in=dull_medicines)

def sendMatchEmail(petition):

	body = "Le informamos que se encuentran disponibles las "+str(petition.cantidad)+" undidades de "+petition.medicamento.nombre+" qué solicito en su peticion N°"+str(petition.id)

	email = EmailMessage('Ya puede buscar su '+petition.medicamento.nombre, body, to=[petition.user.email])
	email.send()
	
