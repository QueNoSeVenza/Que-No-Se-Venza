from django.conf.urls import url
from .models import *
from .views import *

urlpatterns = [
    url(r'^verificacion/$', menu, name='menu'),
    url(r'^stock', stock, name='stock'),
    url(r'^verificacion/input/(?P<case>.+)/$', input_view, name='input_view'),
    url(r'^verificacion/entrada', entrada, name='entrada'),
    url(r'^verificacion/salida', salida, name='salida'),


]