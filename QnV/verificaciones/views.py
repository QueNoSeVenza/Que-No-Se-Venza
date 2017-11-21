# -*- coding: utf-8 -*-
#Usando caracteres no ASCII
from django.shortcuts import render
from .models import *
import datetime
from datetime import date
from donaciones.models import *
from django.http import HttpResponseForbidden,HttpResponseRedirect
from donaciones.matchutils import *
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.contrib import messages
from django.http import JsonResponse

donacionesStore = []

def delete_stock(request):

    itemid = request.GET.get('itemid', None)
    print("Entro el ajax ",itemid)
    item = MedicamentoDonado.objects.get(pk=itemid)
    print(item.stock)
    item.stock = "Inactivo"
    print(item.stock)
    item.save()
    data = {}
    return JsonResponse(data)

def stock (request):
	global donacionesStore
	donacionesStore = []
	if request.user.groups.filter(name='Verificadores').exists():
		stores = Store.objects.all()
		for store in stores:
			if request.user.groups.filter(name=store.nombre).exists():
				medicamentos = MedicamentoDonado.objects.all()
				for i in medicamentos:
					if i.store.nombre == store.nombre:
						donacionesStore.append(i)
				cant = len(medicamentos)
				return render(request,'stock.html',{'donaciones' : donacionesStore, 'cantidad' : cant})
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
	global donacionesStore
	if request.method == "POST":
		print donacionesStore
		meds = [x for x in donacionesStore if str(x.id) == request.POST['donation_id']]
		nombre = request.POST['nome']
		vencimiento = request.POST['date']
		prescripcion  = request.POST['prescripcion']
		medicamento_donado = meds[0]
		fechaV = datetime.strptime(str(medicamento_donado.fecha_vencimiento), '%Y-%m-%d').strftime('%d/%m/%Y')

		tipo_kwargs = {
			'nombre' : request.POST['type'],
		}

		tipo = Tipo.objects.get(**tipo_kwargs)

		try:
			fecha = datetime.strptime(vencimiento, '%d-%m-%Y').strftime('%Y-%m-%d')
		except:
			try:
				fecha = datetime.strptime(vencimiento, '%d/%m/%Y').strftime('%Y-%m-%d')
			except:
				messages.info(request, 'Fecha no Valida!')
				return render(request,'entrada.html',{'donacion' : medicamento_donado, 'fecha' : fechaV})

		fechaVen = datetime.strptime(fecha,'%Y-%m-%d').date()

		if fechaVen <= date.today():
			messages.info(request, 'Fecha no Valida!')
			return render(request,'entrada.html',{'donacion' : medicamento_donado, 'fecha' : fechaV})

		med_donado = medicamento_donado
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
		if len(getMatches(med_donado)) != 0:
			for peticion in getMatches(med_donado):
				sendMatchEmail(peticion)
		return HttpResponseRedirect("/verificacion/stock")
	else:
		try:
			print "das", donacionesStore
			meds = [x for x in donacionesStore if str(x.id) == request.GET['id']]
			print meds
			medicamento_donado = meds[0]
		except (ObjectDoesNotExist,ValueError):
			medicamento_donado = MedicamentoDonado(stock = 'empty')

		print(medicamento_donado.stock)
		if medicamento_donado.stock == 'En Espera':
			fechaV = datetime.strptime(str(medicamento_donado.fecha_vencimiento), '%Y-%m-%d').strftime('%d/%m/%Y')
			return render(request,'entrada.html',{'donacion' : medicamento_donado, 'fecha' : fechaV})

		elif medicamento_donado.stock == 'Disponible' or medicamento_donado.stock == 'Reservado' or medicamento_donado.stock == 'Entregado':
			return HttpResponse("<script>alert('Medicamento ya verificado'); window.location = '/verificacion/input/entrada';</script>")
		else:
			return HttpResponse("<script>alert('Código no valido'); window.location = '/verificacion/input/entrada';</script>")


def salida(request):
	global donacionesStore
	if request.method == "POST":
#       code = request.POST['donation_id']
#       donacion = [x for x in MedicamentoDonado.objects.all() if x.codigo() == code]
#		donacion = MedicamentoDonado.objects.get(pk=request.POST['donation_id'].upper())
		donacion_list = [x for x in donacionesStore if str(x.id) == request.POST['donation_id']]
		donacion = donacion_list[0]

		if donacion.prescripcion == True:
			print("primero")
			if len(request.POST.getlist('checks')) == 1:
				donacion.stock = 'Entregado'
				donacion.verificador_salida = request.user
				donacion.save()

				return HttpResponse("<script>alert('Operacion realizada con exito'); window.location = '/verificacion/input/retiro';</script>")

			else:
				#Cambiar /entrada/input por un template de error
				print("No se han verificado todos los campos, la operación ha sido cancelada")
				return HttpResponse("<script>alert('Operacion cancelada, el medicamento sigue reservado, pero no sera entregado hasta que el usuario presente prescripcion'); window.location = '/verificacion/input/retiro';</script>")
		else:
			donacion.stock = 'Entregado'
			donacion.verificador_salida = request.user
			donacion.save()
			return HttpResponse("<script>alert('Operacion realizada con exito'); window.location = '/verificacion/input/retiro';</script>")
	else:
		code = request.GET['salida']
		try:
			donacion_list = [x for x in donacionesStore if x.codigo() == code]
			donacion = donacion_list[0]
		except IndexError:
			donacion = MedicamentoDonado(stock = 'empty')

		if donacion.stock == "Reservado":
			return render(request,'salida.html',{'donation_id' : donacion.id,'donacion' : donacion})
		else:
			return HttpResponse("<script>alert('Código no valido'); window.location = '/verificacion/input/retiro';</script>")

def search(request):
	if request.method == "POST":

		search = request.POST.get('search1', "")
		check = request.POST.getlist('fooby')

		operaciones = { 'todo': 'todo', 'stock': 'enStock', 'noVerificado': 'noVerificado'}

		try:
			if search == "" and operaciones[check[0]] == "todo":
				return HttpResponseRedirect("/verificacion/stock")
			else:
				if search == "":
					return HttpResponseRedirect("/verificacion/stock/"+operaciones[check[0]])
				else:
					return HttpResponseRedirect("/verificacion/stock/"+operaciones[check[0]]+"/"+search)
		except:
			print("Esa no vale")
			return HttpResponse("<script>alert('Código no valido'); window.location = '/verificacion/stock';</script>")


def todo(request, string):
	global donacionesStore
	meds = donacionesStore
	print meds
	medicamentosMatch = []

	for i in meds:
		if string.upper() in i.medicamento.nombre.upper():
			medicamentosMatch.append(i)
		elif string.upper()  in i.laboratorio.upper():
			medicamentosMatch.append(i)
		elif string.upper() in i.tipo.nombre.upper():
			medicamentosMatch.append(i)

	return render(request,'stock.html',{'donaciones' : medicamentosMatch})


def enStock(request, string):
	global donacionesStore
	print "pone ", donacionesStore
	meds = [x for x in donacionesStore if str(x.verificador_ingreso) != "None" and str(x.verificador_salida) == "None"]
	medicamentosMatch = []
	
	for i in meds:
		if string.upper() in i.medicamento.nombre.upper():
			medicamentosMatch.append(i)
		elif string.upper() in i.laboratorio.upper():
			medicamentosMatch.append(i)
		elif string.upper() in i.tipo.nombre.upper():
			medicamentosMatch.append(i)

	return render(request,'stock.html',{'donaciones' : medicamentosMatch})


def todoStock(request):
	global donacionesStore
	print "pene" , donacionesStore
	meds = [x for x in donacionesStore if str(x.verificador_ingreso) != "None" and str(x.verificador_salida) == "None" and x.store]
	return render(request,'stock.html',{'donaciones' : meds})


def noVerificado(request, string):
	global donacionesStore
	meds = [x for x in donacionesStore if str(x.verificador_ingreso) == "None"]
	medicamentosMatch = []

	for i in meds:
		if string.upper() in i.medicamento.nombre.upper():
			medicamentosMatch.append(i)
		elif string.upper() in i.laboratorio.upper():
			medicamentosMatch.append(i)
		elif string.upper() in i.tipo.nombre.upper():
			medicamentosMatch.append(i)

	return render(request,'stock.html',{'donaciones' : medicamentosMatch})


def todoNoVerificado(request):
	global donacionesStore
	meds = [x for x in donacionesStore if str(x.verificador_ingreso) == "None"]
	return render(request,'stock.html',{'donaciones' : meds})