from django.conf.urls import url
from .models import *
from .views import *

urlpatterns = [
    #New url(r'^$', precentacion, name='precentacion'),
    url(r'^$', login1, name='login1'),
    #url(r'^loguin/', login1, name='login1'),
    url(r'^loguin', log, name='log'),
    url(r'^register', reg, name='reg'),
]