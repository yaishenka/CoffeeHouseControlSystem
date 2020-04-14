from django.contrib import admin
from .models import AbstractProduct, Purchase


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    date_hierarchy = 'time'


admin.site.register(AbstractProduct)