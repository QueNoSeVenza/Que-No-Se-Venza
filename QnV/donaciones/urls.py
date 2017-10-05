from django.conf.urls import url
from .views import *
from django.contrib.auth import views

urlpatterns = [
    url(r'^principal', principal, name='principal'),
    url(r'^donar', donar, name='donar'),
    url(r'^pedir', pedir, name='pedir'),
    url(r'^thanks/(?P<id_med_donado>\d+)', thanks, name='thanks'),
    url(r'^thanks2/', thanks2, name='thanks2'),
    url(r'^ajax/validate_medicamento/$', validate_medicamento, name='validate_medicamento'),
    url(r'^log_out', views.logout, {'next_page': '/'}, name='log_out'),
]
