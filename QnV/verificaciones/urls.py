from django.conf.urls import url
from .models import *
from .views import *

urlpatterns = [
    url(r'^verificacion/stock$', stock, name='stock'),
	url(r'^verificacion/stock/todo/(?P<string>[\w\-]+)', todo, name='todo'),
	url(r'^verificacion/stock/enStock/(?P<string>[\w\-]+)', enStock, name='enStock'),
	url(r'^verificacion/stock/noVerificado/(?P<string>[\w\-]+)', noVerificado, name='noVerificado'),
	url(r'^verificacion/stock/enStock', todoStock, name='todoStock'),
	url(r'^verificacion/stock/noVerificado', todoNoVerificado, name='todoNoVerificado'),
    url(r'^verificacion/input/(?P<case>.+)/$', input_view, name='input_view'),
    url(r'^verificacion/entrada', entrada, name='entrada'),
    url(r'^verificacion/salida', salida, name='salida'),
	url(r'^verificacion/search', search, name='search'),
	url(r'^ajax/delete_stock', delete_stock, name='delete_stock')



]
