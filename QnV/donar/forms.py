from django import forms
from django.contrib.auth.models import User
from donar.models import Medicamento



class MedicamentoForm(forms.ModelForm):
	class Meta:
		model = Medicamento
		fields = ['nombre','concentracion_gramos','cantidad','laboratorio','fecha_vencimiento', 'tipo', 'prescripcion']