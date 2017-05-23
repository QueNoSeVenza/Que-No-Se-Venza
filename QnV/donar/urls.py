from django.conf.urls import url
from .models import *
from .views import *

urlpatterns = [
    url(r'^donar', donar, name='donar'),
    url(r'^pedir', pedir, name='pedir'),    
	url(r'^thanks', thanks, name='thanks'),
]