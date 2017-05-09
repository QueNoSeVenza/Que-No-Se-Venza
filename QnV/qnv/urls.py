from django.conf.urls import url
from .models import *
from .views import *

urlpatterns = [
    url(r'^$', login1, name='login1'),
    url(r'^log', log, name='log'),
    url(r'^reg', reg, name='reg'),
]