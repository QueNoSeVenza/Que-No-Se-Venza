# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.template import loader
from django.views import generic
from .models import *
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect

# Create your views here.
def login(request):
    template = loader.get_template('login.html')
    context = {}
    return HttpResponse(template.render(context, request))

def log(request):
    if 'POST' in request.method:
        usern = request.POST['username']
        passw = request.POST['password']
        print usern + passw
        user = authenticate(username=usern, password=passw)
        if user is not None:
            login(request, user)
            return redirect('/principal')
        else:
            #messages.add_message(request, messages.INFO, 'Usuario o contraseña incorrecta!')
            print "hola"
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def reg(request):
    if 'POST' in request.method:
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['pass']
        u = User.objects.filter(username=email)
        if u is not None:
            user = User.objects.create_user(email, email, password)
            user.first_name = name
            user.save()
            userant = authenticate(username=email, password=password)
            if userant is not None:
                login(request, userant)
                return redirect('/principal')
            else:
                messages.add_message(request, messages.INFO, 'Algo salio mal')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.add_message(request, messages.INFO, 'Ese usuario ya esta en uso')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))