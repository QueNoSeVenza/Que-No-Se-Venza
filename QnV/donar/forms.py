from django import forms
from django.contrib.auth.models import User
<<<<<<< HEAD
from qnv.models import *
=======
from qnv.models import Medicamento, Pedir
>>>>>>> da1b7acaba4e4234c89500a06fba0180cccc9bc2



class MedicamentoForm(forms.ModelForm):
	class Meta:
		model = Medicamento
		fields = ['nombre','concentracion_gramos','cantidad','laboratorio','fecha_vencimiento', 'tipo', 'prescripcion']

class PeticionForm(forms.ModelForm):
	class Meta:
		model = Pedir
		fields = ['user','medicamento']
