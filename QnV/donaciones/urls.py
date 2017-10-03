from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^principal', principal, name='principal'),
    url(r'^donar', donar, name='donar'),
    url(r'^matchs/(?P<pid>\d+)/$', matchs, name='matchs'),    
    url(r'^pedir', pedir, name='pedir'),
	url(r'^thanks', thanks, name='thanks'),
    url(r'^ajax/validate_medicamento/$', validate_medicamento, name='validate_medicamento'),	
]
