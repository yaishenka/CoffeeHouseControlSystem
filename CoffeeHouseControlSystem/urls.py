from django.contrib import admin
from django.conf.urls import include
from django.views.generic import TemplateView
from django.urls import path
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='base.html'), name='home'),
    path('users/', include('users.urls')),
    path('accounting/', include('accounting.urls')),
]