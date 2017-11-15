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
from django.contrib.auth import authenticate
from donaciones.matchutils import *
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.http import JsonResponse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.utils.datastructures import MultiValueDictKeyError
from django.views.generic.list import ListView
from django.template import RequestContext


@login_required(login_url='/login/')

def principal(request):
    template = loader.get_template('index.html')
    verificador = False
    medicamentos = Medicamento.objects.all()
    user = request.user
    print user
    donations = len(MedicamentoDonado.objects.filter(donacion__user=user))
    por_entregar = len(MedicamentoDonado.objects.filter(donacion__user=user, stock='En Espera'))
    donations_done = len(MedicamentoDonado.objects.filter(donacion__user=user, stock='Entregado'))

   # por_entregar = len([x for x in MedicamentoDonado.objects.all() if str(x.MedicamentoDonado.stock) == "None"])

    if request.user.groups.filter(name='Verificadores').exists():
        verificador = True
    context = {'verificador':verificador, 'django_users':user,'medi' : medicamentos, 'donacion': donations, 'por_entregar': por_entregar, 'donacion_done': donations_done, }
    return HttpResponse(template.render(context, request))

def thanks2(request):
    template = loader.get_template('thanks2.html')
    context = {}
    return HttpResponse(template.render(context, request))

def thanks(request, id_med):
    template = loader.get_template('thanks.html')
    medicamentoDonado = MedicamentoDonado.objects.get(pk=id_med)
    context = {'medDona': medicamentoDonado}
    email = EmailMessage('Codigo de donacion','Tu codigo de donacion es '+id_med, to=[medicamentoDonado.donacion.user.email])
    email.send()

    return HttpResponse(template.render(context, request))


##############################################################################

def donar(request):

    if 'POST' in request.method:
        #Capturando argumentos del request para cada objeto a crear.
        mes = request.POST['mes']

        fecha_vencimiento =  mes+request.POST['anio']

        medicamento_kwargs = {
            'nombre' : request.POST['donar_nombre'].upper(),
            'concentracion_gramos' : request.POST['donar_concentracion_gramos'],
            'droga' : request.POST['donar_droga'].upper()
        }

        medicamento_donado_kwargs = {
            'cantidad' : request.POST['donar_cantidad'],
            'tipo' : request.POST['donar_tipo'].upper(),
            'laboratorio' : request.POST['donar_laboratorio'].upper() ,
            'fecha_vencimiento' : datetime.strptime(fecha_vencimiento,
                                            '%m%Y').date(),
        }

        donacion_kwargs = {
        'user' : request.user,
        }

        gramos = medicamento_kwargs['concentracion_gramos']
        cantidad = medicamento_donado_kwargs['cantidad']

        if gramos <= "0" or cantidad <= "0":

            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if medicamento_donado_kwargs['fecha_vencimiento'] <= date.today():
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
        id_med = str(nuevo_medicamento_donado.id)
        return redirect('/thanks/'+id_med)
    else:
        return redirect('/principal')

def validate_medicamento(request):
    nombre = request.GET.get('nombre', None)
    print(nombre)
    concentracion_gramos = request.GET.get('concentracion', None)
    print(concentracion_gramos)
    print(Medicamento.objects.filter(nombre=nombre.upper(),concentracion_gramos=concentracion_gramos))
    data = {
        'exists': Medicamento.objects.filter(nombre=nombre.upper(),concentracion_gramos=concentracion_gramos).exists()
    }
    return JsonResponse(data)

def pedir(request):

    if 'POST' in request.method:
        #Capturando argumentos para un Pedido y su Medicamento
        try:
            similar_flag = request.POST['similar']
        except MultiValueDictKeyError:
            similar_flag = 'off'
        medicamento_kwargs = {
            'nombre' :  request.POST['pedir_nombre'].upper(),
            'concentracion_gramos' : request.POST['pedir_gramos'],
            'droga' : request.POST['pedir_droga'].upper(),
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
            return redirect('/matchs/'+similar_flag+'/'+str(nuevo_pedido.id))
        else:
            return redirect('/thanks2')



 

def matchs(request,case,pid):

    if "POST" in request.method:
        mid = request.POST['match']
        pedido = Pedido.objects.get(pk=pid)
        donacion = MedicamentoDonado.objects.get(pk=mid)
        match = Match(pedido=pedido,donacion=donacion)
        match.save()
        pedido.estado = "Emparejado"
        donacion.stock = "Reservado"
        pedido.save()
        donacion.save()
        return redirect('/code/'+donacion.codigo())

    else:
        if case == 'on':

            matchs = getSimilarMatches(Pedido.objects.get(pk = pid))

        else:

            matchs = getMatches(Pedido.objects.get(pk = pid))

        return render(request,'matchs.html',{'matchs' : matchs, 'pid': pid,'case' : case})


def code(request,id):
    d_id = id
    try:
        donacion_list = [x for x in MedicamentoDonado.objects.all() if x.codigo() == d_id]
        donacion = donacion_list[0]
    except IndexError:
        donacion = MedicamentoDonado(stock = 'empty')
    print(donacion.stock)
    if donacion.stock == "Reservado":
        if donacion.prescripcion == True:
            email = EmailMessage('Codigo de pedido','Recuerda que para retirar este medicamento es necesario que presentes su debida prescripcion. Tu codigo de pedido es '+d_id.upper(), to=[donacion.donacion.user.email])
            email.send()
            return render(request,'code.html',{'donation' : donacion,'donation_id' : d_id.upper()})
        elif donacion.prescripcion == False:
            email = EmailMessage('Codigo de pedido','Tu codigo de pedido es '+d_id.upper(), to=[donacion.donacion.user.email])
            email.send()
            return render(request,'code.html',{'donation' : donacion,'donation_id' : d_id.upper()})            
    else:
        return HttpResponse("<script>alert('Código no valido'); window.location = '/verificacion/input/retiro';</script>")
    
    def logout(request):
        logout(request)
        return HttpResponseRedirect("/")
