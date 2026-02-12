from django.contrib import admin
from . import models


admin.site.register(models.Collection)

# admin.site.register(models.Product)
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title' , 'unit_price']
    list_editable = ['unit_price']
    list_per_page = 10