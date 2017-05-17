from django.shortcuts import render
from donar.models import Medicamento
from donar.forms import MedicamentoForm
from django.http import HttpResponseRedirect,HttpResponse

def donar (request):
	form = MedicamentoForm()
	if request.method == 'POST':
		form = MedicamentoForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/thanks')
			print(Medicamento.objects.all())
		else:
			form = MedicamentoForm()
	return render(
		request,
		'donar.html',
		{'form' : form}
)

def thanks (request):
	return render(
		request,
		'thanks.html',
		{}
)