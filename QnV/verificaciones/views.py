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
		donaciones = Donacion.objects.all()
		return render(request,'stock.html',{'donaciones' : donaciones})
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

		print(request.POST['donation_id'])
		print(len(request.POST.getlist('checks')))

		if len(request.POST.getlist('checks')) == 3:
			funcion  = request.POST['funcion']
			prescripcion  = request.POST['prescripcion']	
			print(funcion)
			donacion = Donacion.objects.get(pk = request.POST['donation_id'])
			donacion.medicamento.funcion = funcion
			donacion.stock = "Disponible"
			donacion.save()
			donacion.medicamento.save()
 			#Cambiar /entrada/input por un template que comunique el exito de la operación
			print("Donación registrada con exito")
			return HttpResponseRedirect("/verificacion/")

		else:
			#Cambiar /entrada/input por un template de error
			print("No se han verificado todos los campos, la operación ha sido cancelada")			
			return HttpResponseRedirect("/verificacion/input/entrada")


	else:

		donacion = Donacion.objects.get(pk = request.GET['id'])

		if donacion.stock == "Pendiente":
			return render(request,'entrada.html',{'donacion' : donacion})
		else:
			#Cambiar /entrada/input por un template que avise que esta donación ya se encuentra en Stock
			print("Esta donación ya se encuentra en stock")
			return HttpResponseRedirect("/verificacion/input/entrada")

def salida(request):


	if request.method == "POST":

		print(request.POST['donation_id'])
		print(len(request.POST.getlist('checks')))

		if len(request.POST.getlist('checks')) == 3:
			funcion  = request.POST['funcion']
			print(funcion)
			donacion = Donacion.objects.get(pk = request.POST['donation_id'])
			donacion.medicamento.funcion = funcion
			donacion.stock = "Disponible"
			donacion.save()
			donacion.medicamento.save()
 			#Cambiar /entrada/input por un template que comunique el exito de la operación
			print("Donación registrada con exito")
			return HttpResponseRedirect("/verificacion/")

		else:
			#Cambiar /entrada/input por un template de error
			print("No se han verificado todos los campos, la operación ha sido cancelada")			
			return HttpResponseRedirect("/verificacion/input/entrada")


	else:

		donacion = Donacion.objects.get(pk = request.GET['id'])

		if donacion.stock == "Pendiente":
			return render(request,'salida.html',{'donacion' : donacion})
		else:
			#Cambiar /entrada/input por un template que avise que esta donación ya se encuentra en Stock
			print("Esta donación ya se encuentra en stock")
			return HttpResponseRedirect("/verificacion/input/entrada")
