from django.contrib import admin
from django.conf.urls import include
from django.views.generic import TemplateView
from django.urls import path
from .views import create_purchase, view_purchase, add_order_position, view_all_purchases

urlpatterns = [
    path('create/', create_purchase, name='create_purchase'),
    path('list/', view_all_purchases, name='list'),
    path('<uuid:purchase_uid>/view/', view_purchase, name='view_purchase'),
    path('<uuid:purchase_uid>/add_position/', add_order_position, name='add_position')

]