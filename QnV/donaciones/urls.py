from django.conf.urls import url
from .views import *
from django.contrib.auth import views
from django.contrib.auth.views import logout
from donaciones import views  #entregar


urlpatterns = [
    url(r'^principal', principal, name='principal'),
    url(r'^donar', donar, name='donar'),
    url(r'^matchs/(?P<case>.+)/(?P<pid>\d+)/$', matchs, name='matchs'), 
    url(r'^code/(?P<id>.+)/$', code, name='code'),           
    url(r'^pedir', pedir, name='pedir'),
    url(r'^thanks/(?P<id_med>\d+)', thanks, name='thanks'),
    url(r'^thanks2', thanks2, name='thanks2'),
    url(r'^ajax/validate_medicamento', validate_medicamento, name='validate_medicamento'),
    url(r'^logout/$', logout, name='logout')
]
