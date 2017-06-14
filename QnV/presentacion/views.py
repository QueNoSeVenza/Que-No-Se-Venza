# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.template import loader
from django.shortcuts import render
from .models import *
from django.http import HttpResponseRedirect, HttpResponse

# Create your views here.
def presentacion(request):
    template = loader.get_template('presentacion.html')
    context = {}
    return HttpResponse(template.render(context, request))