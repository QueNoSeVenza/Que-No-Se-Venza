# -*- coding: utf-8 -*-
from django.shortcuts import render
from .models import *
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect,HttpResponse
from django.template import loader

def principal(request):
    template = loader.get_template('index.html')
    verificador = False
    if request.user.groups.filter(name='Verificadores').exists():
        verificador = True
    context = {'verificador':verificador}
    return HttpResponse(template.render(context, request))


def donar(request):
    if 'POST' in request.method:
        donar_nombre = request.POST['donar_nombre']            
        donar_concentracion_gramos = request.POST['donar_concentracion_gramos']
        donar_cantidad = request.POST['donar_cantidad']
        donar_laboratorio = request.POST['donar_laboratorio']
        donar_fecha_vencimiento = request.POST['donar_fecha_vencimiento']
        donar_tipo = request.POST['donar_tipo']
        donar_droga = request.POST['donar_droga']
        author = request.user
        
        med_donar = [donar_nombre,donar_concentracion_gramos,donar_cantidad,donar_laboratorio,donar_fecha_vencimiento,donar_tipo,donar_droga]
        
        if Medicamento.objects.filter(nombre=med_donar[0], concentracion_gramos=med_donar[1], laboratorio=med_donar[3]).exists():
            print "if"
            medicamento_guardado = Medicamento.objects.get(nombre=med_donar[0], concentracion_gramos=med_donar[1], laboratorio=med_donar[3])
            guardarDonacion(request, med_donar, medicamento_guardado)
            return redirect('/principal')
        else:
            print "else"
            guardarMedicamento(request, med_donar)
            return redirect('/principal')
            
            
def pedir(request):
    if 'POST' in request.method:
        medicamento_pedido = request.POST['medicamento_pedido']
        author = request.user
        medicamento_objeto = Medicamento.objects.get(nombre=medicamento_pedido)
        pedir_save = Pedir(user=author,
                          medicamento=medicamento_objeto)
        pedir_save.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def thanks(request):
	return render(
		request,
		'thanks.html',
		{}
)


def guardarDonacion(request, med_donar, medicamento_guardado):
    donacion = Donacion(medicamento=medicamento_guardado,
                            user=request.user,
                            cantidad=med_donar[2],
                            fecha_vencimiento=med_donar[4])
    donacion.save()
    return redirect('/donar_index')


def guardarMedicamento(request, med_donar):
    medicamento = Medicamento(nombre=med_donar[0],
                            concentracion_gramos=med_donar[1],
                            laboratorio=med_donar[3],
                            droga=med_donar[6],
                            tipo=med_donar[5])
    medicamento.save()
    medicamento_guardado = Medicamento.objects.get(id=medicamento.id)
    guardarDonacion(request, med_donar, medicamento_guardado)