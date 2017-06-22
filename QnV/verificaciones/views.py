# -*- coding: utf-8 -*- 
#Usando caracteres no ASCII
from django.shortcuts import render
from .models import *
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
		medicamentos = MedicamentoDonado.objects.all()
		print(medicamentos)
		return render(request,'stock.html',{'string' : string,'medicamentos' : medicamentos})
	else:

		return HttpResponseForbidden()



def input_view (request,case):

	if request.user.groups.filter(name='Verificadores').exists():

		string = "Verificador! ;)"

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
			donacion = Medicamento.objects.get(pk = request.POST['donation_id'])
			donacion.funcion = funcion
			donacion.stock = True
			donacion.save()
			print(donacion.funcion)
 			#Cambiar /entrada/input por un template que comunique el exito de la operación
			print("Donación registrada con exito")
			return HttpResponseRedirect("/verificar/input/entrada/")

		else:
			#Cambiar /entrada/input por un template de error
			print("No se han verificado todos los campos, la operación ha sido cancelada")			
			return HttpResponseRedirect("/verificar/input/entrada")


	else:

		donacion = Medicamento.objects.get(pk = request.GET['id'])

		if donacion.stock == False:
			return render(request,'entrada.html',{'donacion' : donacion})
		else:
			#Cambiar /entrada/input por un template que avise que esta donación ya se encuentra en Stock
			print("Esta donación ya se encuentra en stock")
			return HttpResponseRedirect("/verificar/input/entrada")
