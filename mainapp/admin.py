from django.contrib import admin

from .models import Type_of_Product,Users,Product,Cart,Inventory

admin.site.register(Type_of_Product)
admin.site.register(Users)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Inventory)
