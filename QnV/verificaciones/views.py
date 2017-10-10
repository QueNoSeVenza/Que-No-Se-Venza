# -*- coding: utf-8 -*-
#Usando caracteres no ASCII
from django.shortcuts import render
from .models import *
from donaciones.models import *
from django.http import HttpResponseForbidden,HttpResponseRedirect

def menu (request):
	string = ""

	if request.user.groups.filter(name='Verificadores').exists():
		string = "Verificador! ;)"
		return render(request,'menu.html',{'string' : string})
	else:

		return HttpResponseForbidden()


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
		
		nombre = request.POST['nombre']
		vencimiento = request.POST['fechaven']
		prescripcion  = request.POST['prescripcion']
		tipo = request.POST['tipo_verifacion']

		med_donado = MedicamentoDonado.objects.get(pk=request.POST['donation_id'])
		med_donado.fecha_vencimiento = vencimiento
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
		d_id = request.POST['donation_id']
		print(len(request.POST.getlist('checks')))
		donacion = MedicamentoDonado.objects.get(id = d_id)
		code = request.POST['salida']
		obj_med_donado = MedicamentoDonado.objects.all()
		for i in obj_med_donado:

			if str(i.codigo()) == str(code):

				donacion = i

		#donacion = MedicamentoDonado.objects.get(pk=request.POST['donation_id'])
		if donacion.medicamento.prescripcion == True:
			if len(request.POST.getlist('checks')) == 1:
				donacion.stock = 'Entregado'
				donacion.verificador_salida = request.user
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
		code = request.POST.get('salida', False)
		obj_med_donado = MedicamentoDonado.objects.all()

		for i in obj_med_donado:
			if i.codigo() == code:

				donacion = i



		#donacion = MedicamentoDonado.objects.get(pk = d_id )

		if donacion.stock == "Reservado":
			return render(request,'salida.html',{'donation_id' : d_id,'donacion' : donacion})
		else:
			#Cambiar /entrada/input por un template que avise que esta donación ya se encuentra en stock
			print("Esta donación ya se encuentra en stock")
			return HttpResponseRedirect("/verificacion/input/entrada")
