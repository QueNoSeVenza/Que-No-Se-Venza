# -*- coding: utf-8 -*-
from django.shortcuts import render
from qnv.models import *
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
        m_prescripcion = request.POST['m_prescripcion']
        m_droga = request.POST['m_droga']
        author = request.user
        
        #comparar medicamento con nombre, concentracion y/o (opcional) laboratorio
        medicamneto_tabla = Medicamento.objects.get(nombre=m_nombre,
                                                    concentracion_gramos=m_concentracion_gramos,
                                                    laboratorio=m_laboratorio)
        
        #if exist:
        if medicamento is not None:
            #crear donacio y pasar objeto medicamneto a la tabla donacion
            donacion_save = Donacion(medicamento=medicamneto_tabla,
                                    user=author,
                                    cantidad=m_cantidad,
                                    fecha_vencimiento=m_fecha_vencimiento)
            donacion_save.save()
            return redirect('/thanks')
        #else:
        else:
            #crer objeto en tabla medicamneto y crear tabla donacion
            medicamento_nuevo = Medicamento(nombre=m_nombre,
                                           concentracion_gramos=m_concentracion_gramos,
                                           laboratorio=m_laboratorio,
                                           droga=m_droga,
                                           prescripcion=m_prescripcion,
                                           tipo=m_tipo)
            
            id_medicamento_nuevo = Medicamento.objects.get(id=medicamento_nuevo.id)
            
            donacion_nueva = Donacion(medicamento=id_medicamento_nuevo,
                                     user=author,
                                     cantidad=m_cantidad,
                                     fecha_vencimiento=m_fecha_vencimiento)
            
            medicamento_nuevo.save()
            donacion_nueva.save()
            return redirect('/thanks')


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
