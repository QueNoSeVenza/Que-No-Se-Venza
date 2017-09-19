from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib import admin
from donaciones.models import *

# Create your models here.
class VerificarIngreso(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    medicamento = models.ForeignKey(MedicamentoDonado, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

class VerificarRetiro(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    medicamento = models.ForeignKey(MedicamentoDonado, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)