from django.contrib import admin
from . import models


admin.site.register(models.Collection)

# admin.site.register(models.Product)
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title' , 'unit_price' , 'inventory_status' , 'collection_title' ]
    list_editable = ['unit_price']
    list_per_page = 10
    list_select_related = ['collection']

    #for custom column
    @admin.display(ordering= 'inventory')
    def inventory_status(self , product):
        if product.inventory < 50:
            return 'Low'
        return 'OK'
    
    def collection_title(self , product):
        return product.collection.title
@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name' , 'last_name' , 'membership']
    list_per_page = 10
    list_editable = ['membership']
    ordering = ['first_name' , 'last_name'] #Only affects the Django admin

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id' , 'placed_at' , 'customer'] 
    list_per_page = 10   


