# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib import admin

from Medicamento.models import Medicamento
from Donacion.models import Donacion

import random
# Create your models here.
r_1 = (1, 1000)
r_2 = (1, 64)
r_m = (1,12)
r_a = (2017,2999)

med_1 = Medicamento(nombre='GRIPABEN',
                   concentracion_gramo=random.choices(r_1),
                   laboratorio='SAVANT',
                   droga='PARACETAMOL',
                   funcion='Analgesico',
                   prescripcion=False,
                   tipo='Pastillas')
med_1.save()

med_2 = Medicamento(nombre='CLARIFRIOL',
                   concentracion_gramo=random.choices(r_1),
                   laboratorio='VANINER S.A',
                   droga='FLUOXETINA',
                   funcion='Analgesico',
                   prescripcion=False,
                   tipo='Pastillas')
med_2.save()

med_3 = Medicamento(nombre='EBURNATE',
                   concentracion_gramo=random.choices(r_1),
                   laboratorio='MSD ARGENTINA',
                   droga='ENALEPADRIN',
                   funcion='Analgesico',
                   prescripcion=False,
                   tipo='Pastillas')
med_3.save()

class Medicamento(models.Model):
    nombre = models.CharField(max_length=60)
    concentracion_gramos = models.CharField(max_length=60)
    laboratorio = models.CharField(max_length=60)
    droga = models.CharField(max_length=60)
    FUNCION_FARMACEUTICA = (
        ('Analgesico', 'Analgesico'),
        ('Androgenos', 'Androgenos'),
    )
    funcion = models.CharField(max_length=60, choices=FUNCION_FARMACEUTICA, default="Null")
    prescripcion = models.BooleanField(default=False)
    TIPO = (
        ('Pastillas', 'Pastillas'),
        ('Jarabe', 'Jarabe'),
        ('Gotas', 'Gotas'),
    )
    tipo = models.CharField(max_length=60, choices=TIPO, default=0)
    #cantidad = models.CharField(max_length=60)

    def __unicode__(self):
        return self.nombre

class Donacion(models.Model):
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cantidad = models.CharField(max_length=60)
    fecha_vencimiento = models.DateField()
    stock = models.CharField(max_length=60, default="En Espera")
    
class Pedir(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
