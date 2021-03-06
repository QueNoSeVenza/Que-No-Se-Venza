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
        if len(getMatches(med_donado)) != 0:
            for peticion in getMatches(med_donado):
                sendMatchEmail(peticion)
        return HttpResponseRedirect("/verificacion/stock")
            
    else:
        print(Donacion.objects.all().values('id'))
        try:
            medicamento_donado = MedicamentoDonado.objects.get(id = request.GET['id'])
        except (ObjectDoesNotExist,ValueError):
            medicamento_donado = MedicamentoDonado(stock = 'empty')

        print(medicamento_donado.stock)


        if medicamento_donado.stock == 'En Espera':
            return render(request,'entrada.html',{'donacion' : medicamento_donado})
        
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
		search = request.POST['search1']
		meds = MedicamentoDonado.objects.all()
		medicamentosMatch = []
		
		for i in meds:
			if search in i.medicamento.nombre:
				medicamentosMatch.append(i)
				
		return render(request,'stock.html',{'donaciones' : medicamentosMatch})
