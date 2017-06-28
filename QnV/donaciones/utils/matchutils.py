# -*- coding: utf-8 -*-
from datetime import datetime
from .models import *
from django.core import mail

def getMatches(entity):

	if entity.__class__.__name__ == "Pedido":

		not_dull_medicines = [medicamento.id for medicamento in MedicamentoDonado.objects.all() if medicamento.isDull() == False]
		return MedicamentoDonado.objects.filter(medicamento=entity.medicamento, id__in=not_dull_medicines).order_by('fecha_vencimiento')
	
	elif entity.__class__.__name__ == "MedicamentoDonado":

		return MedicamentoDonado.objects.filter(medicamento=entity.medicamento)


def executeMatch(petition):

	match_list = getMatches(petition)
	
	for match in match_list:
		match.cantidad -= petition.cantidad
		if match.cantidad >= 0:

			match.save()

		else: 

			petition.cantidad = abs(match.cantidad)



def getDullMedicines():
	
	dull_medicines = [medicamento.id for medicamento in MedicamentoDonado.objects.all() if medicamento.isDull() == False]
	return MedicamentoDonado.objects.filter(id__in=dull_medicines)

def sendMatchEmail(match, user):
	
