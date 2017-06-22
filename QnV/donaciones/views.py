# -*- coding: utf-8 -*-
from django.shortcuts import render
from .models import *
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect,HttpResponse
from django.template import loader
from django.utils import timezone
from datetime import datetime
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
        #Capturando argumentos del request para cada objeto a crear.
        fecha_vencimiento =  request.POST.get('mes')+"/"+request.POST.get('anio')

        medicamento_kwargs = {
            'nombre' : request.POST['donar_nombre'],
            'concentracion_gramos' : request.POST['donar_concentracion_gramos'],
            'laboratorio' : request.POST['donar_laboratorio'] ,
            'droga' : request.POST['donar_droga']
        }

        medicamento_donado_kwargs = {

        'cantidad' : request.POST['donar_cantidad'],
        'fecha_vencimiento' : datetime.datetime.strptime(request.POST.get('mes')+
                                        request.POST.get('anio'),
                                            '%m%Y').date(),

        }

        donacion_kwargs = {

        'user' : request.user,

        }
        
        #Intentando seleccionar el Medicamento generico.
        
         
        

        #Si ya existe un Medicamento para medicamento_donado simplemente lo guardo.
        if Medicamento.objects.filter(**medicamento_kwargs).exists():

            medicamento_guardado = Medicamento.objects.get(**medicamento_kwargs)

            nueva_donacion = Donacion(**donacion_kwargs)
            nueva_donacion.save()

            medicamento_donado_kwargs['donacion'] = nueva_donacion
            medicamento_donado_kwargs['medicamento'] = medicamento_guardado 

            nuevo_medicamento_donado = MedicamentoDonado(**medicamento_donado_kwargs)
            nuevo_medicamento_donado.save()
 
        #De lo contrario, además guardo un medicamento.
        else:

            nuevo_medicamento = Medicamento(**medicamento_kwargs)
            nuevo_medicamento.save()

            nueva_donacion = Donacion(**donacion_kwargs)
            nueva_donacion.save()

            medicamento_donado_kwargs['donacion'] = nueva_donacion
            medicamento_donado_kwargs['medicamento'] = medicamento_guardado 

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
        pedir_nombre = request.POST['pedir_nombre']
        pedir_gramos = request.POST['pedir_gramos']
        pedir_cantidad = request.POST['pedir_cantidad']
        author = request.user
        
        array_pedido = [pedir_nombre,pedir_gramos,pedir_cantidad]
        fechas_medicamento = []
        
        
        if Medicamento.objects.filter(nombre=arry_pedido[0], concentracion_gramos=arry_pedido[1]).exists():
            
            medicamento_pedido = Medicamento.objects.get(nombre=arry_pedido[0], concentracion_gramos=arry_pedido[1])
            print( medicamento_pedido)
            
            donaciones_medicamento = medicamento_donado.objects.filter(medicamento=medicamento_pedido)
            print( donaciones_medicamento)
        
            for a in donaciones_medicamento:
                print( a)
                if timezone.now().date() < a.fecha_vencimiento: 
                    fechas_medicamento.append(a.fecha_vencimiento)
            
            print( fechas_medicamento)
            
            fe = fechas_medicamento[0]
            print( fe)
            
            for b in fechas_medicamento:
                print( b)
                if fe > b:
                    print( "if")
                    fe = b
            
            print( fe)
            
            return redirect('/thanks')
        else:
            print( "else)")
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