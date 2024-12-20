from io import BytesIO
from django.core.files import File
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager
from PIL import Image

from django.core.validators import RegexValidator
from django.utils.text import slugify


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


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name}'
    
    def get_absolute_url(self):
        return f'/{self.slug}'

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8,decimal_places=2)
    category = models.ForeignKey(Category,related_name='products',on_delete=models.CASCADE)
    description = models.TextField(blank=True,null=True)
    slug = models.SlugField(default="",null=False)
    date_posted = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='uploads/',blank=True,null=True)
    thumbnail = models.ImageField(upload_to='uploads/',blank=True,null=True)

    class Meta:
        ordering = ['-date_posted']
    
    def save(self,*args,**kwargs):
        self.slug = slugify(self.name)
        super().save(*args,**kwargs)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f'/{self.category.slug}/{self.slug}/'
    
    def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8000' + self.image.url
        return ''
    
    def get_thumbnail(self):
        if self.thumbnail:
            return 'http://127.0.0.1:8000' + self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
                return 'http://127.0.0.1:8000' + self.thumbnail.url
            else:
                return ''
            
    def make_thumbnail(self,image,size=(300,200)): 
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io,'JPEG',quality=85)

        thumbnail = File(thumb_io,name=image.name)

        return thumbnail



class Order(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='order')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField()
    address = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=255)
    place = models.CharField(max_length=255)
    phone = models.CharField(max_length=255, validators=[RegexValidator(regex=r'^(06|05|07|03)\d{8}$', message='Enter a valid phone number')])
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at',]

    def __str__(self):
        return self.first_name    


class OrderItem(models.Model):
    order = models.ForeignKey(Order,related_name='items',on_delete=models.CASCADE)
    product = models.ForeignKey(Product,related_name='items',on_delete=models.CASCADE)        
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return '%s' % self.id