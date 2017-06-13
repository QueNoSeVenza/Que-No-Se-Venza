from django.conf.urls import url
from .models import *
from .views import *

urlpatterns = [
    url(r'^menu', menu, name='menu'),
    url(r'^stock', stock, name='stock'),
    url(r'^input/(?P<case>.+)/$', input_view, name='input_view'),
    url(r'^entrada/', entrada, name='entrada'),


]
