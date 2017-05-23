from django import forms
from django.contrib.auth.models import User
from qnv.models import *




class MedicamentoForm(forms.ModelForm):
	class Meta:
		model = Medicamento
		fields = ['nombre','concentracion_gramos','cantidad','laboratorio','fecha_vencimiento', 'tipo', 'prescripcion']

class PeticionForm(forms.ModelForm):
	class Meta:
		model = Pedir
		fields = ['user','medicamento']
