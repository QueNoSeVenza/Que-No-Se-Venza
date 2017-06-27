# -*- coding: utf-8 -*-
from django.shortcuts import render
from .models import *
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect,HttpResponse
from django.template import loader
from django.utils import timezone
from datetime import datetime
import datetime
import donaciones.matchutils

def principal(request):
    template = loader.get_template('index.html')
    verificador = False
    if request.user.groups.filter(name='Verificadores').exists():
        verificador = True
    context = {'verificador':verificador}
    return HttpResponse(template.render(context, request))

def donar(request):

    if 'POST' in request.method:
        #Capturando argumentos del request para cada objeto a crear.
        fecha_vencimiento =  request.POST.get('mes')+request.POST.get('anio')

        medicamento_kwargs = {
            'nombre' : request.POST['donar_nombre'],
            'concentracion_gramos' : request.POST['donar_concentracion_gramos'],
            'laboratorio' : request.POST['donar_laboratorio'] ,
            'droga' : request.POST['donar_droga']
        }

        medicamento_donado_kwargs = {
        'cantidad' : request.POST['donar_cantidad'],
            
        'fecha_vencimiento' : datetime.datetime.strptime(fecha_vencimiento,
                                            '%m%Y').date()
        }

        donacion_kwargs = {
        'user' : request.user,
        }   

        
        #Si ya existe un Medicamento para medicamento_donado simplemente lo guardo.
        try:

            medicamento_guardado = Medicamento.objects.get(**medicamento_kwargs)
            nueva_donacion = Donacion(**donacion_kwargs)
            nueva_donacion.save()

            medicamento_donado_kwargs['donacion'] = nueva_donacion
            medicamento_donado_kwargs['medicamento'] = medicamento_guardado 

            nuevo_medicamento_donado = MedicamentoDonado(**medicamento_donado_kwargs)
            nuevo_medicamento_donado.save()
 
        #De lo contrario, además guardo un medicamento.
        except Medicamento.DoesNotExist:

            nuevo_medicamento = Medicamento(**medicamento_kwargs)
            nuevo_medicamento.save()

            nueva_donacion = Donacion(**donacion_kwargs)
            nueva_donacion.save()

            medicamento_donado_kwargs['donacion'] = nueva_donacion
            medicamento_donado_kwargs['medicamento'] = nuevo_medicamento

            nuevo_medicamento_donado = MedicamentoDonado(**medicamento_donado_kwargs)
            nuevo_medicamento_donado.save()   



        return redirect('/thanks')
                        

def thanks(request):
	return render(
		request,
		'thanks.html',
		{}
)

def pedir(request):

    if 'POST' in request.method:
        #Capturando argumentos para un Pedido y su Medicamento
        medicamento_kwargs = {

            'nombre' :  request.POST['pedir_nombre'],
            'concentracion_gramos' : request.POST['pedir_gramos'], 

        }

        pedido_kwargs = {

            'user' : request.user,
            'cantidad' : request.POST['pedir_cantidad'],

        }

        #Intento crear el Pedido con un Medicamento existente.
        try:

            pedido_kwargs['medicamento'] = Medicamento.objects.get(**medicamento_kwargs)
            nuevo_pedido = Pedido(**pedido_kwargs)
            nuevo_pedido.save()



        #En caso de que lo anterior no funcione creo un Pedido y su Medicamento.
        #Deberiamos implementar un AJAX para verificar esto y agregar al form 
        #los campos restantes de medicamento.
        
        except Medicamento.DoesNotExist():

            nuevo_medicamento = Medicamento(**medicamento_kwargs)
            nuevo_medicamento.save()
            pedido_kwargs['medicamento'] = nuevo_medicamento
            nuevo_pedido = Pedido(**pedido_kwargs)
            nuevo_pedido.save()            

        #Cambiar /thanks por la siguiente url del proceso de peticion.
        getMatches(nuevo_pedido)
        return redirect('/thanks')
