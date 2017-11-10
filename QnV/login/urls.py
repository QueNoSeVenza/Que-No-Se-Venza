from django.conf.urls import url
from .models import *
from .views import *
from django.conf.urls import include
from django.contrib.auth.views import login, logout_then_login, password_reset, password_reset_done, password_reset_confirm, password_reset_complete, LogoutView
from django.core.urlresolvers import reverse_lazy

urlpatterns = [
    url(r'^login', login, name='login'),
    url(r'^tyc', tyc, name='tyc'),
    url(r'^log', log, name='log'),
    url(r'^reg', reg, name='reg'),  
    url(r'^logout/$', log_out, name='log_out')
]
