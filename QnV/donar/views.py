# -*- coding: utf-8 -*-
from django.shortcuts import render
from qnv.models import *
from .forms import MedicamentoForm, PeticionForm
from django.http import HttpResponseRedirect,HttpResponse

def donar (request):
	form = MedicamentoForm()
	if request.method == 'POST':
		form = MedicamentoForm(request.POST)
		if form.is_valid():
			form.save()
			print("Entra")
			medicamentos = Medicamento.objects.all()
			for i in medicamentos:
				print(i.nombre)
			return HttpResponseRedirect('/thanks')
		else:
			form = MedicamentoForm()
	return render(
		request,
		'donar.html',
		{'form' : form}
)

def pedir (request):
	form = PeticionForm()
	if request.method == 'POST':
		form = PeticionForm(request.POST)
		if form.is_valid():
			form.save()
			print("Entra")
			return HttpResponseRedirect('/thanks')
			print(Pedir.objects.all())
		else:
			print("Invalid form")
			form = PeticionForm()
	return render(
		request,
		'pedir.html',
		{'form' : form}
)


def thanks (request):
	return render(
		request,
		'thanks.html',
		{}
)
