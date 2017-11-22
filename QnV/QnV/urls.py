"""QnV URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include
from django.contrib.auth.views import  password_reset, password_reset_done, password_reset_confirm, password_reset_complete
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('login.urls', namespace='login')),
    url(r'^', include('donaciones.urls', namespace='donaciones')),
    url(r'^', include('verificaciones.urls', namespace='verificaciones')),
    url(r'^', include('presentacion.urls', namespace='presentacion')),
    url(r'^reset/password_reset', password_reset,
        {'template_name':'password_reset_form.html',
         'email_template_name': 'password_reset_email.html'},
        name='password_reset'),

    url(r'^password_reset_done', password_reset_done,
        {'template_name': 'password_reset_done.html'},
        name='password_reset_done'),

    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
        password_reset_confirm,
        {'template_name': 'password_reset_confirm.html'},
        name='password_reset_confirm'
       ),

    url(r'^reset/done', password_reset_complete, {'template_name': 'password_reset_complete.html'},
        name='password_reset_complete'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
