# -*- coding: utf-8 -*-
from django.shortcuts import render
from qnv.models import *
from .forms import *
from django.http import HttpResponseRedirect,HttpResponse

def donar (request):
	form = MedicamentoForm()
	if request.method == 'POST':
		form = MedicamentoForm(request.POST)
		if form.is_valid():
			form.save()
			print(Medicamento.objects.all())
			return HttpResponseRedirect('/thanks')
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