from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Medicamento)
admin.site.register(MedicamentoDonado)
admin.site.register(Donacion)
admin.site.register(Pedir)