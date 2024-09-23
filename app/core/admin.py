from django.contrib import admin
from .models import Tag,Product,Order,CustomUser

admin.site.register(CustomUser)
admin.site.register(Tag)
admin.site.register(Product)
admin.site.register(Order)