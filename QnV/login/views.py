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
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.sessions.models import Session
# Create your views here.
def login(request):
    '''
    template = loader.get_template('login.html')
    all_users = User.objects.all()
    context = {
        'django_users' : all_users
    }
    return HttpResponse(template.render(context, request))
    '''
    all_users = User.objects.all()
    context = {
        'django_users' : all_users
    }
    return render(request, 'login.html', context)


def tyc(request):
    return render(request, 'tyc.html', {})

def log(request):
    if 'POST' in request.method:
        usern = request.POST['username']
        passw = request.POST['password']
        print(usern + passw)
        user = authenticate(request, username=usern, password=passw)
        if user is not None:
            auth_login(request, user)
            return redirect('/principal')
        else:
            messages.add_message(request, messages.INFO, 'Usuario y/o contraseña incorrecta!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('/login')

def reg(request):
    if 'POST' in request.method:
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['pass1']
        password2 = request.POST['pass2']
        u = User.objects.filter(username=email)
        terms = request.POST.get('terms', False)
        if u is not None:
            if terms == "on":
                if u.exists():
                    messages.add_message(request, messages.INFO, 'Ese email ya esta en uso')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                else:

                    user = User.objects.create_user(email, email, password)
                    user.first_name = name
                    user.save()
                    userant = authenticate(username=email, password=password)
                    if userant is not None:
                        auth_login(request, userant)
                        return redirect('/principal')
                    else:
                        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                messages.add_message(request, messages.INFO, 'Debe aceptar los terminos y condiciones')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    else:
        return redirect('/login')
