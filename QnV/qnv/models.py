# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib import admin
# Create your models here.

class Medicamento(models.Model):
    FUNCION_FARMACEUTICA = (
        ('Analgesico', 'Analgesico'),
        ('Androgenos', 'Androgenos'),
    )
    funcion = models.CharField(max_length=60, choices=FUNCION_FARMACEUTICA, default="Null")
    PRESCRIPCION_MEDICA = (
        ('Con Receta','Con Receta'),
        ('Sin Receta','Sin Receta'),
    )
    prescripcion = models.CharField(max_length=60, choices=PRESCRIPCION_MEDICA, default=0)
    TIPO = (
        ('Pastillas', 'Pastillas'),
        ('Jarabe', 'Jarabe'),
        ('Gotas', 'Gotas'),
    )
    nombre = models.CharField(default = '',max_length=60)
    tipo = models.CharField(max_length=60, choices=TIPO, default=0)
    concentracion_gramos = models.CharField(max_length=60)
    cantidad = models.CharField(max_length=60)
    laboratorio = models.CharField(max_length=60)
    fecha_vencimiento = models.DateField()
    stock = models.BooleanField(default=False)
   
    def __unicode__(self):
        return self.nombre


class Donacion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE)

class Pedir(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE)
    
class VerificarIngreso(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE)
    
class VerificarRestiro(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE)
