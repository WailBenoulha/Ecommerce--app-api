from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.IntegerField()
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name','last_name','phone_number']

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
class Tag(models.Model):
    name = models.CharField(max_length=255,unique=True)
    
    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    tag = models.ManyToManyField(Tag)
    create_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='products')
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Order(models.Model):
    date_order = models.DateTimeField(default=timezone.now)
    product = models.ManyToManyField(Product)
    order_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='order')