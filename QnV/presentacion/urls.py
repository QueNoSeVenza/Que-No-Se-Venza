from django.conf.urls import url
from .models import *
from .views import *

urlpatterns = [ 
    url(r'^$', presentacion, name='presentacion'),
    url(r'^municipalidad-de-mendiolaza' , municipalidad, name='municipalidad'),
    
]