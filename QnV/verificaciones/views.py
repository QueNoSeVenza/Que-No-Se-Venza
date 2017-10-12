# -*- coding: utf-8 -*-
#Usando caracteres no ASCII
from django.shortcuts import render
from .models import *
import datetime
from datetime import date
from donaciones.models import *
from django.http import HttpResponseForbidden,HttpResponseRedirect
from donaciones.matchutils import *

#def menu (request):
#	string = ""
#
#	if request.user.groups.filter(name='Verificadores').exists():
#		string = "Verificador! ;)"
#		return render(request,'menu.html',{'string' : string})
#	else:
#
#		return HttpResponseForbidden()


def stock (request):

	if request.user.groups.filter(name='Verificadores').exists():
		string = "Verificador! ;)"
		verificador_ingreso =[]
		medicamentos = MedicamentoDonado.objects.all()
		print(medicamentos)
		return render(request,'stock.html',{'string' : string,'donaciones' : medicamentos})
	else:

		return HttpResponseForbidden()



def input_view (request,case):

	if request.user.groups.filter(name='Verificadores').exists():

		if case == "entrada":

			return render(request,'entrada_input.html',{})

		elif case == "retiro":

			return render(request,'retiro_input.html',{})


	else:

		return HttpResponseForbidden()




def entrada(request):
	if request.method == "POST":

		nombre = request.POST['nome']
		vencimiento = request.POST['date']
		prescripcion  = request.POST['prescripcion']
		tipo = request.POST['type']

		if vencimiento[:3] == "Sep":
			nuevo = vencimiento[:3]+vencimiento[4:]
		else :
			nuevo = vencimiento

		try:
			fecha = datetime.strptime(nuevo, '%b. %d, %Y').strftime('%Y-%m-%d')
		except:
			try: 
				fecha = datetime.strptime(nuevo, '%B %d, %Y').strftime('%Y-%m-%d')
			except:
				try:
					fecha = datetime.strptime(nuevo, '%d-%m-%Y').strftime('%Y-%m-%d')
				except:
					fecha = datetime.strptime(nuevo, '%d/%m/%Y').strftime('%Y-%m-%d')


		med_donado = MedicamentoDonado.objects.get(pk=request.POST['donation_id'])
		med_donado.fecha_vencimiento = fecha
		med_donado.medicamento.nombre = nombre
		med_donado.tipo = tipo
		med_donado.prescripcion = prescripcion
		med_donado.verificador_ingreso = request.user
		med_donado.stock = "Disponible"
		med_donado.save()
		med_donado.medicamento.save()


		#Cambiar /entrada/input por un template que comunique el exito de la operación
		print("Donación registrada con exito")
		return HttpResponseRedirect("/verificacion/")


	else:
		print(Donacion.objects.all().values('id'))

		medicamento_donado = MedicamentoDonado.objects.get(id = request.GET['id'])
		print(medicamento_donado.stock)


		if medicamento_donado.stock == 'En Espera':
			return render(request,'entrada.html',{'donacion' : medicamento_donado})
		else:
			#Cambiar /entrada/input por un template que avise que esta donación ya se encuentra en stock
			print("Esta donación ya se encuentra en stock")
			return HttpResponseRedirect("/verificacion/input/entrada")

def salida(request):

	if request.method == "POST":
#		code = request.POST['donation_id']
#		donacion = [x for x in MedicamentoDonado.objects.all() if x.codigo() == code]
		donacion = MedicamentoDonado.objects.get(pk=request.POST['donation_id'])

		if donacion.prescripcion == True:
			if len(request.POST.getlist('checks')) == 1:
				donacion.stock = 'Entregado'
				donacion.verificador_salida = request.user
				pedido.estado = "Entregado"
				pedido.save()
				donacion.save()

				return HttpResponseRedirect("/verificacion/")

			else:
				#Cambiar /entrada/input por un template de error
				print("No se han verificado todos los campos, la operación ha sido cancelada")
				return HttpResponseRedirect("/verificacion/input/entrada")
		else:
			donacion.stock = 'Entregado'
			donacion.verificador_salida = request.user
			donacion.save()
			return HttpResponseRedirect("/verificacion/")
	else:
		code = request.GET['salida']
		donacion = [x for x in MedicamentoDonado.objects.all() if x.codigo() == code]
		print donacion

		if donacion[0].stock == "Reservado":
			return render(request,'salida.html',{'donation_id' : donacion[0].id,'donacion' : donacion[0]})
		else:
			#Cambiar /entrada/input por un template que avise que esta donación ya se encuentra en stock
			print("Este codigo no existe")
			return HttpResponseRedirect("/verificacion/input/entrada")
