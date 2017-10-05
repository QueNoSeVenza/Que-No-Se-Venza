from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^principal', principal, name='principal'),
    url(r'^donar', donar, name='donar'),
    url(r'^pedir', pedir, name='pedir'),
    url(r'^thanks2/', thanks2, name='thanks2'),
    url(r'^ajax/validate_medicamento/$', validate_medicamento, name='validate_medicamento'),
    url(r'^log_out', log_out, name='log_out'),
]
