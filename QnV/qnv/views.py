# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.template import loader
from django.shortcuts import render
from qnv.models import *
from django.http import HttpResponseRedirect, HttpResponse

# Create your views here.
def precentacion(request):
    template = loader.get_template('index.html')
    context = {}
    return HttpResponse(template.render(context, request))