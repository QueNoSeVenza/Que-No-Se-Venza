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
        author = request.user
        medicamento_save = Medicamento(prescripcion=m_prescripcion,
                                       nombre=m_nombre,
                                       tipo=m_tipo,
                                       concentracion_gramos=m_concentracion_gramos,
                                       cantidad=m_cantidad,
                                       laboratorio=m_laboratorio,
                                       fecha_vencimiento=m_fecha_vencimiento)
        medicamento_save.save()
        medicamento_id_objeto = Medicamento.objects.get(id=medicamento_save.id)
        donacion_save = Donacion(user=author,
                                medicamento=medicamento_id_objeto)
        donacion_save.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def pedir(request):
    if 'POST' in request.method:
        medicamento_pedido = request.POST['medicamento_pedido']
        author = request.user
        pedir_save = Pedir(user=author,
                          medicamento=medicamento_pedido)
        pedir_save.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def thanks(request):
	return render(
		request,
		'thanks.html',
		{}
)
