# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.template import loader
from django.shortcuts import render
from django.shortcuts import redirect
from .models import *
from django.http import HttpResponseRedirect, HttpResponse

# Create your views here.
def presentacion(request):
    template = loader.get_template('presentacion.html')
    context = {}
    return HttpResponse(template.render(context, request))

def municipalidad(request):
    return redirect("http://www.municipiomendiolaza.com.ar/")

def mensaje(request):
    return HttpResponse("<script>alert('Su mensaje fue enviado, gracias por colaborar con QNV'); window.location = '/';</script>")