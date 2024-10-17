from django.contrib import admin
from .models import Product,Order,CustomUser,Category

admin.site.register(CustomUser)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Category)