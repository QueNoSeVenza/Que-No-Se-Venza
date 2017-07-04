from django.conf.urls import url
from .models import *
from .views import *

urlpatterns = [
    url(r'^login', login, name='login'),
    url(r'^log', log, name='log'),
    url(r'^reg', reg, name='reg'),
    # url(r'^validate_email',validate_email, name='validate_email')
]
