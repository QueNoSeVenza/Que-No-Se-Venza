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

	if request.user.groups.filter(name='Verificadores').exists():
		verificador_ingreso =[]
		fechaV = []
		medicamentos = MedicamentoDonado.objects.all()
		cant = len(medicamentos)
		for i in medicamentos:
			fechaV.append(datetime.strptime(str(i.fecha_vencimiento), '%Y-%m-%d').strftime('%d/%m/%Y'))
			if i.isDull() == True:
				print(i.stock)
				i.stock = "Vencido"
				i.save()
		return render(request,'stock.html',{'donaciones' : medicamentos, 'fecha' : fechaV, 'cantidad' : cant})
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
		ndi = request.POST['donation_id']
		nombre = request.POST['nome']
		vencimiento = request.POST['date']
		prescripcion  = request.POST['prescripcion']
		tipo = request.POST['type']
		medicamento_donado = MedicamentoDonado.objects.get(id = ndi)
		fechaV = datetime.strptime(str(medicamento_donado.fecha_vencimiento), '%Y-%m-%d').strftime('%d/%m/%Y')

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
		if len(getMatches(med_donado)) != 0:
			for peticion in getMatches(med_donado):
				sendMatchEmail(peticion)
		return HttpResponseRedirect("/verificacion/stock")
	else:
		try:
			medicamento_donado = MedicamentoDonado.objects.get(id = request.GET['id'])
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
    if request.method == "POST":
#       code = request.POST['donation_id']
#       donacion = [x for x in MedicamentoDonado.objects.all() if x.codigo() == code]
        donacion = MedicamentoDonado.objects.get(pk=request.POST['donation_id'].upper())

        if donacion.prescripcion == True:
            if len(request.POST.getlist('checks')) == 1:
                donacion.stock = 'Entregado'
                donacion.verificador_salida = request.user
                donacion.save()

                return HttpResponseRedirect("/verificacion/input/retiro")

            else:
                #Cambiar /entrada/input por un template de error
                print("No se han verificado todos los campos, la operación ha sido cancelada")
                return HttpResponseRedirect("/verificacion/input/retiro")
        else:
            donacion.stock = 'Entregado'
            donacion.verificador_salida = request.user
            donacion.save()
            return HttpResponseRedirect("/verificacion/input/retiro")
    else:
        code = request.GET['salida']
        try:
            donacion_list = [x for x in MedicamentoDonado.objects.all() if x.codigo() == code]
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
	meds = MedicamentoDonado.objects.all()
	medicamentosMatch = []

	for i in meds:
		if string in i.medicamento.nombre:
			medicamentosMatch.append(i)
		elif string in i.laboratorio:
			medicamentosMatch.append(i)
		elif string in i.tipo:
			medicamentosMatch.append(i)

	return render(request,'stock.html',{'donaciones' : medicamentosMatch})


def enStock(request, string):
	meds = [x for x in MedicamentoDonado.objects.all() if str(x.verificador_ingreso) != "None" and str(x.verificador_salida) == "None"]
	medicamentosMatch = []

	for i in meds:
		if string in i.medicamento.nombre:
			medicamentosMatch.append(i)
		elif string in i.laboratorio:
			medicamentosMatch.append(i)
		elif string in i.tipo:
			medicamentosMatch.append(i)

	return render(request,'stock.html',{'donaciones' : medicamentosMatch})


def todoStock(request):
	meds = [x for x in MedicamentoDonado.objects.all() if str(x.verificador_ingreso) != "None" and str(x.verificador_salida) == "None"]
	return render(request,'stock.html',{'donaciones' : meds})


def noVerificado(request, string):
	meds = [x for x in MedicamentoDonado.objects.all() if str(x.verificador_ingreso) == "None"]
	medicamentosMatch = []

	for i in meds:
		if string in i.medicamento.nombre:
			medicamentosMatch.append(i)
		elif string in i.laboratorio:
			medicamentosMatch.append(i)
		elif string in i.tipo:
			medicamentosMatch.append(i)

	return render(request,'stock.html',{'donaciones' : medicamentosMatch})


def todoNoVerificado(request):
	meds = [x for x in MedicamentoDonado.objects.all() if str(x.verificador_ingreso) == "None"]
	return render(request,'stock.html',{'donaciones' : meds})
