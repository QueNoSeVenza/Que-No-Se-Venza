# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import *
from django.contrib import admin

# Register your models here.
admin.site.register(Medicamento)
admin.site.register(Donacion)
admin.site.register(Pedir)
admin.site.register(VerificarIngreso)
admin.site.register(VerificarRetiro)