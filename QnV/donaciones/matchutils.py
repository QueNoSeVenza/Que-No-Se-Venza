# -*- coding: utf-8 -*-
from datetime import datetime
from .models import *
from django.core import mail
from django.core.mail import EmailMessage

#Esta funcion devuelve una lista de MedicamentosDonados que comparten campo medicamento con el pedido
#que se use como argumento solo si hay suficientes unidades para satisfacerlo.

def getMatches(entity):
	print("GETMATCHES>",entity.__class__.__name__)
	if entity.__class__.__name__ == "Pedido":

		print(entity)
		not_dull_medicines = [medicamento.id for medicamento in MedicamentoDonado.objects.all() if medicamento.isDull() == False]
		match_list = MedicamentoDonado.objects.filter(medicamento=entity.medicamento, id__in=not_dull_medicines,stock="Disponible").order_by('fecha_vencimiento')
		quantities = [medicamento.cantidad for medicamento in match_list]
		print(match_list,"MATCHLIST")

		print(match_list)
		return match_list

	elif entity.__class__.__name__ == "MedicamentoDonado":

		print("MATCHMD")
		match_list = Pedido.objects.filter(medicamento=entity.medicamento,estado="Activo")
		print("<>",match_list)
		return match_list

def getSimilarMatches(entity):
		not_dull_medicines = [medicamento.id for medicamento in MedicamentoDonado.objects.all() if medicamento.isDull() == False]
		match_list = MedicamentoDonado.objects.filter(medicamento__droga=entity.medicamento.droga, id__in=not_dull_medicines,stock="Disponible").order_by('fecha_vencimiento')
		quantities = [medicamento.cantidad for medicamento in match_list]
		print(not_dull_medicines,match_list,quantities)

		print(match_list)
		return match_list
#Esta funcion reserva la cantidad del pedido a uno o varios MedicamentoDonado, en caso de
#necesitar reservar parcialmente un MedicamentoDonado le sustrae la cantidad necesaria y
#se crea otro MedicamentDonado con esa cantidad y el estado "Reservado".

#Requiere que se le pase un Pedido y devuelve una lista de (MedicamentoDonado,cantidad).

def executeMatch(petition):

	substaction_values = []
	match_list = getMatches(petition)

	match_obj = Match(pedido = petition)
	match_obj.save()


	for match in match_list:

		quantity = match.cantidad
		quantity -= petition.cantidad

		if quantity > 0:

			print("#1 Block")

			match.cantidad -= petition.cantidad
			match.save()
			kept_medicine = match
			kept_medicine.cantidad = petition.cantidad
			kept_medicine.stock = "Reservado"
			kept_medicine.pk = None
			kept_medicine.save()
			match_obj.medicamentos.add(kept_medicine)
			match_obj.save()
			print("<<<<<<<<<<<zzzzzzzz",match_obj.medicamentos.all())

			return match_obj

		else:

			print("#2 Block")

			substaction_values.append((match,match.cantidad))
			petition.cantidad = abs(quantity)
			match.stock = "Reservado"
			match.save()
			match_obj.medicamentos.add(match)
			print("<<<<",match_obj.medicamentos.all())
			match_obj.save()
			if petition.cantidad == 0:
				return match_obj




#Devuelve una lista de los medicamentos vencidos.

def getDullMedicines():

	dull_medicines = [medicamento.id for medicamento in MedicamentoDonado.objects.all() if medicamento.isDull() == False]
	return MedicamentoDonado.objects.filter(id__in=dull_medicines)


def sendMatchEmail(pedido):

	body = "Alguien ha donado "+str(pedido.medicamento)+". Quizas este disponnible para reservarlo, haga click en esta url para continuar: http://127.0.0.1:8000/matchs/"+str(pedido.id)

	email = EmailMessage('Alguien ha donado '+str(pedido.medicamento), body, to=[pedido.user.email])
	email.send()
