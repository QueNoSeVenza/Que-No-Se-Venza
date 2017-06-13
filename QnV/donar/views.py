# -*- coding: utf-8 -*-
from django.shortcuts import render
from qnv.models import *
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect,HttpResponse
from django.template import loader

def donar_index(request):
    template = loader.get_template('index.html')
    context = {}
    return HttpResponse(template.render(context, request))


def donar(request):
    if 'POST' in request.method:
        m_nombre = request.POST['m_nombre']            
        m_concentracion_gramos = request.POST['m_concentracion_gramos']
        m_cantidad = request.POST['m_cantidad']
        m_laboratorio = request.POST['m_laboratorio']
        m_fecha_vencimiento = request.POST['m_fecha_vencimiento']
        m_tipo = request.POST['m_tipo']
        m_droga = request.POST['m_droga']
        author = request.user
        
        arry = [m_nombre,m_concentracion_gramos,m_cantidad,m_laboratorio,m_fecha_vencimiento,m_tipo,m_droga]
        
        if Medicamento.objects.filter(nombre=arry[0], concentracion_gramos=arry[1], laboratorio=arry[3]).exists():
            print "if"
            medicamento_guardado = Medicamento.objects.get(nombre=arry[0], concentracion_gramos=arry[1], laboratorio=arry[3])
            guardarDonacion(request, arry, medicamento_guardado)
        else:
            print "else"
            guardarMedicamento(request, arry)
            
            
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


def guardarDonacion(request, arry, medicamento_guardado):
    donacion = Donacion(medicamento=medicamento_guardado,
                            user=request.user,
                            cantidad=arry[2],
                            fecha_vencimiento=arry[4])
    donacion.save()
    return redirect('/donar_index')


def guardarMedicamento(request, arry):
    medicamento = Medicamento(nombre=arry[0],
                            concentracion_gramos=arry[1],
                            laboratorio=arry[3],
                            droga=arry[6],
                            tipo=arry[5])
    medicamento.save()
    medicamento_guardado = Medicamento.objects.get(id=medicamento.id)
    guardarDonacion(request, arry, medicamento_guardado)