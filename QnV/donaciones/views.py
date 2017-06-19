# -*- coding: utf-8 -*-
from django.shortcuts import render
from .models import *
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect,HttpResponse
from django.template import loader
from django.utils import timezone
import datetime

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
        donar_fecha_vencimiento = (request.POST.get('mes')+"/"+request.POST.get('anio'))
        donar_tipo = request.POST.get('donar_tipo')
        donar_droga = request.POST['donar_droga']
        author = request.user
         
        print(request.POST.get('mes'),request.POST.get('anio'))
        
        med_donar = [donar_nombre,donar_concentracion_gramos,donar_cantidad,donar_laboratorio,donar_fecha_vencimiento,donar_tipo,donar_droga]
        print med_donar
        
        if Medicamento.objects.filter(nombre=med_donar[0], concentracion_gramos=med_donar[1], laboratorio=med_donar[3]).exists():
            print "if"
            medicamento_guardado = Medicamento.objects.get(nombre=med_donar[0], concentracion_gramos=med_donar[1], laboratorio=med_donar[3])
            guardarDonacion(request, med_donar, medicamento_guardado)
            
            return redirect('/thanks')
        else:
            print "else"
            guardarMedicamento(request, med_donar)
            return redirect('/thanks')
                        
def guardarMedicamento(request, med_donar):
    print "med"
    medicamento = Medicamento(nombre=med_donar[0],
                            concentracion_gramos=med_donar[1],
                            laboratorio=med_donar[3],
                            droga=med_donar[6],
                            tipo=med_donar[5])
    medicamento.save()
    medicamento_guardado = Medicamento.objects.get(id=medicamento.id)
    guardarDonacion(request, med_donar, medicamento_guardado)

def guardarDonacion(request, med_donar, medicamento_guardado):
    print "dona"
    donacion = Donacion(user=request.user)
    donacion.save()
    donacion_guardada = Donacion.objects.get(id=donacion.id)
    guardarMedicamentoDonado(request, med_donar, medicamento_guardado,donacion_guardada)
    
def guardarMedicamentoDonado(request, med_donar, medicamento_guardado,donacion_guardada):
    print "medDonado"
    print med_donar[4]
    medicamentoDonado = MedicamentoDonado(medicamento=medicamento_guardado,
                                          donacion=donacion_guardada,
                                          cantidad=med_donar[2],
                                          fecha_vencimiento=med_donar[4])
    medicamentoDonado.save()
    
def thanks(request):
	return render(
		request,
		'thanks.html',
		{}
)

def pedir(request):
 


    if 'POST' in request.method:
        pedir_nombre = request.POST['pedir_nombre']
        pedir_gramos = request.POST['pedir_gramos']
        pedir_cantidad = request.POST['pedir_cantidad']
        author = request.user
        
        array_pedido = [pedir_nombre,pedir_gramos,pedir_cantidad]
        fechas_medicamento = []
        
        
        if Medicamento.objects.filter(nombre=arry_pedido[0], concentracion_gramos=arry_pedido[1]).exists():
            
            medicamento_pedido = Medicamento.objects.get(nombre=arry_pedido[0], concentracion_gramos=arry_pedido[1])
            print medicamento_pedido
            
            donaciones_medicamento = MedicamentoDonado.objects.filter(medicamento=medicamento_pedido)
            print donaciones_medicamento
        
            for a in donaciones_medicamento:
                print a
                if timezone.now().date() < a.fecha_vencimiento: 
                    fechas_medicamento.append(a.fecha_vencimiento)
            
            print fechas_medicamento
            
            fe = fechas_medicamento[0]
            print fe
            
            for b in fechas_medicamento:
                print b
                if fe > b:
                    print "if"
                    fe = b
            
            print fe
            
            return redirect('/thanks')
        else:
            print "else"
            return redirect('/thanks')
        
        
        # fecha  LISTO
            # no estar vencido   LISTO
            # tiene que se proxima a el dia msimo LISTO
            
        #
        
        
        
        # cantidad 
            # cantidad total de todas las donaciones del medicamento
            # si es igual o menor
                # restar si es meno o igual 
                # mostrar otras opciones
            # sino 
                # mostrar la cantidad que tengo 
                # mostrar otras opciones
            
            
            
            
            
#        if medicamento_pedido.exists():
#            for m in medicamento_pedido:
#                #
#        medicamento_objeto = Medicamento.objects.get(nombre=arry_pedido[0], concentracion_gramos=arry_pedido[1])
#        pedir_save = Pedir(user=author,
#                          medicamento=medicamento_objeto)
#        pedir_save.save()
#        return redirect('/thanks')