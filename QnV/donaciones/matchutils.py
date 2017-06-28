# -*- coding: utf-8 -*-
from datetime import datetime
from .models import *
from django.core import mail
from django.core.mail import EmailMessage

#Esta funcion devuelve una lista de MedicamentosDonados que comparten campo medicamento con el pedido
#que se use como argumento solo si hay suficientes unidades para satisfacerlo. 

def getMatches(entity):

	if entity.__class__.__name__ == "Pedido":

		not_dull_medicines = [medicamento.id for medicamento in MedicamentoDonado.objects.all() if medicamento.isDull() == False]
		match_list = MedicamentoDonado.objects.filter(medicamento=entity.medicamento, id__in=not_dull_medicines).order_by('fecha_vencimiento')
		quantities = [medicamento.cantidad for medicamento in match_list]
		

		if sum(quantities) >= entity.cantidad:
			return match_list


#Esta funcion reserva la cantidad del pedido a uno o varios MedicamentoDonado, en caso de 
#necesitar reservar parcialmente un MedicamentoDonado le sustrae la cantidad necesaria y
#se crea otro MedicamentDonado con esa cantidad y el estado "Reservado".

#Requiere que se le pase un Pedido y devuelve una lista de (MedicamentoDonado,cantidad).

def executeMatch(petition):

	substaction_values = []
	match_list = getMatches(petition)
	
	for match in match_list:

		quantity = match.cantidad
		quantity -= petition.cantidad

		if quantity >= 0:
			
			print("#1 Block")

			match.cantidad -= petition.cantidad
			match.save()
			kept_medicine = match
			kept_medicine.cantidad = petition.cantidad
			kept_medicine.stock = "Reservado"
			kept_medicine.pk = None
			kept_medicine.save()

			return substaction_values

		else: 

			print("#2 Block")
			
			substaction_values.append((match,match.cantidad))
			petition.cantidad = abs(quantity)
			match.stock = "Reservado"
			match.save()




#Devuelve una lista de los medicamentos vencidos.

def getDullMedicines():
	
	dull_medicines = [medicamento.id for medicamento in MedicamentoDonado.objects.all() if medicamento.isDull() == False]
	return MedicamentoDonado.objects.filter(id__in=dull_medicines)

def sendMatchEmail(petition):

	body = "Le informamos que se encuentran disponibles las "+str(petition.cantidad)+" undidades de "+petition.medicamento.nombre+" qué solicito en su peticion N°"+str(petition.id)

	email = EmailMessage('Ya puede buscar su '+petition.medicamento.nombre, body, to=[petition.user.email])
	email.send()
	
