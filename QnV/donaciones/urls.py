from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^principal', principal, name='principal'),
    url(r'^donar', donar, name='donar'),
    url(r'^pedir', pedir, name='pedir'),
	url(r'^thanks', thanks, name='thanks'),
]