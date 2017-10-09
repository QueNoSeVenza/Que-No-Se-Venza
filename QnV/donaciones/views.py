# -*- coding: utf-8 -*-
from django.shortcuts import render
from .models import *
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect,HttpResponse
from django.template import loader
from django.utils import timezone
from datetime import datetime
import datetime
from datetime import date
from django.contrib.auth import authenticate, logout
from donaciones.matchutils import *
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.http import JsonResponse
from django.contrib import auth
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def principal(request):
    template = loader.get_template('index.html')
    verificador = False
    user = request.user
    if request.user.groups.filter(name='Verificadores').exists():
        verificador = True
    context = {'verificador':verificador, 'django_users':user}
    return HttpResponse(template.render(context, request))

def thanks2(request):
    template = loader.get_template('thanks2.html')
    context = {}
    return HttpResponse(template.render(context, request))


def log_out(request):
    print "saliendo"
    logout(request)
    print "salio "
    return redirect('/login')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


##############################################################################

def donar(request):

    if 'POST' in request.method:
        #Capturando argumentos del request para cada objeto a crear.
        mes = request.POST['mes']

        fecha_vencimiento =  mes+request.POST['anio']

        medicamento_kwargs = {
            'nombre' : request.POST['donar_nombre'],
            'concentracion_gramos' : request.POST['donar_concentracion_gramos'],
            'droga' : request.POST['donar_droga']
        }

        medicamento_donado_kwargs = {
            'cantidad' : request.POST['donar_cantidad'],
            'tipo' : request.POST['donar_tipo'],
            'laboratorio' : request.POST['donar_laboratorio'] ,
            'fecha_vencimiento' : datetime.strptime(fecha_vencimiento,
                                            '%m%Y').date(),
        }

        donacion_kwargs = {
        'user' : request.user,
        }

        gramos = medicamento_kwargs['concentracion_gramos']
        cantidad = medicamento_donado_kwargs['cantidad']

        if gramos <= "0" or cantidad <= "0":
            print "se fue por gramos o cantidad"
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if medicamento_donado_kwargs['fecha_vencimiento'] <= date.today():
            print "se fue por fecha"
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        nuevo_medicamento_donado= ""

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


        for pedido in getMatches(nuevo_medicamento_donado):
            if len(getMatches(pedido)) != 0:
                executeMatch(pedido)
                sendMatchEmail(pedido)
                print("Envio mail")
                
        id_med_donado = str(nuevo_medicamento_donado.id)
        return redirect('/principal')
    else:
        return redirect('/principal')



def validate_medicamento(request):
    nombre = request.GET.get('nombre', None)
    print(nombre)
    concentracion_gramos = request.GET.get('concentracion', None)
    print(concentracion_gramos)
    print(Medicamento.objects.filter(nombre=nombre,concentracion_gramos=concentracion_gramos))
    data = {
        'exists': Medicamento.objects.filter(nombre=nombre,concentracion_gramos=concentracion_gramos).exists()
    }
    return JsonResponse(data)

def pedir(request):

    if 'POST' in request.method:
        #Capturando argumentos para un Pedido y su Medicamento
        medicamento_kwargs = {
            'nombre' :  request.POST['pedir_nombre'],
            'concentracion_gramos' : request.POST['pedir_gramos'],
            'droga' : request.POST['pedir_droga'],
        }

        pedido_kwargs = {
            'user' : request.user,
        }

        #Intento crear el Pedido con un Medicamento existente.
        try:

            pedido_kwargs['medicamento'] = Medicamento.objects.get(**medicamento_kwargs)
            nuevo_pedido = Pedido(**pedido_kwargs)
            nuevo_pedido.save()



        #En caso de que lo anterior no funcione creo un Pedido y su Medicamento.
        #Deberiamos implementar un AJAX para verificar esto y agregar al form
        #los campos restantes de medicamento.

        except Medicamento.DoesNotExist:

            nuevo_medicamento = Medicamento(**medicamento_kwargs)
            nuevo_medicamento.save()
            pedido_kwargs['medicamento'] = nuevo_medicamento
            nuevo_pedido = Pedido(**pedido_kwargs)
            nuevo_pedido.save()

        #Cambiar /thanks por la siguiente url del proceso de peticion.


        print(">>>>>>",nuevo_pedido.id)
        if len(getMatches(nuevo_pedido)) != 0:
            return redirect('/matchs/'+str(nuevo_pedido.id))
        else:
            return redirect('/thanks2')




def matchs(request,pid):

    if "POST" in request.method:
        mid = request.POST['match']
        pedido = Pedido.objects.get(pk=pid)
        donacion = MedicamentoDonado.objects.get(pk=mid)
        match = Match(pedido=pedido,donacion=donacion)
        match.save()
        donacion.stock = "Reservado"
        donacion.save()
        return redirect('/thanks2')

    else:

        matchs = getMatches(Pedido.objects.get(pk = pid))
        return render(request,'matchs.html',{'matchs' : matchs, 'pid': pid})
