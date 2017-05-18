from django.conf.urls import url
from .models import *
from .views import *

urlpatterns = [ 
    url(r'^$', precentacion, name='precentacion'),
]