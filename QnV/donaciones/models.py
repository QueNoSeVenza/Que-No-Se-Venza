# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib import admin
# Create your models here.

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

    def __unicode__(self):
        return self.nombre

class Donacion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    medicamentos = models.ManyToManyField(Medicamento, through='MedicamentoDonado')

class MedicamentoDonado(models.Model):
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE)
    donacion = models.ForeignKey(Donacion, on_delete=models.CASCADE)
    cantidad = models.CharField(max_length=60)
    fecha_vencimiento = models.CharField(max_length=6)
    stock = models.CharField(max_length=60, default="En Espera")
    
class Pedir(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE, related_name="pedidos")
    created = models.DateTimeField(auto_now_add=True)