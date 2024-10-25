from django.contrib import admin
from .models import Product,Order,CustomUser,Category

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','get_absolute_url')
    prepopulated_fields = {'slug':('name',)}



admin.site.register(CustomUser)
admin.site.register(Product,ProductAdmin)
admin.site.register(Order)
admin.site.register(Category)