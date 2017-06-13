from django.conf.urls import url
from qnv.models import *
from .views import *

urlpatterns = [
    url(r'^donar_index', donar_index, name='donar_index'),
    url(r'^donar', donar, name='donar'),
    url(r'^pedir', pedir, name='pedir'),    
	url(r'^thanks', thanks, name='thanks'),
]