from django.conf.urls import url
from .models import *
from .views import *
from django.conf.urls import include
from django.contrib.auth.views import login, logout_then_login, password_reset, password_reset_done, password_reset_confirm, password_reset_complete, LogoutView
from django.core.urlresolvers import reverse_lazy

urlpatterns = [
    url(r'^login', login, name='loni'),
    url(r'^tyc', tyc, name='tyc'),
    url(r'^log', log, name='log'),
    url(r'^reg', reg, name='reg'),  
<<<<<<< HEAD
    
=======
    url(r'^logouts/$', logouts, name='logouts')
>>>>>>> 79f5d9845a5a814de726576a5c656f2ba3af0d90
]
