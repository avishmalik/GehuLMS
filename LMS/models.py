from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser,PermissionsMixin
from django.contrib.auth.models import PermissionsMixin
# Create your models here.
from .manager import CustomUserManager 
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class CustomUser(AbstractBaseUser,PermissionsMixin):
    last_login = None
    # groups = None
    # user_permissions = None
    # id = models.AutoField(primary_key=True)
    # username = None
    email = models.EmailField(max_length=100,unique=True)
    Complete_Name= models.CharField(max_length = 100)
    Department = models.CharField(max_length = 100)
    Role = models.CharField(max_length = 100)
    # phone_number = models.CharField(max_length=10)
    is_staff = models.BooleanField(default= False)
    is_active = models.BooleanField(default= True)
    is_member = models.BooleanField(default = True)
    is_hod = models.BooleanField(default = False)
    is_director = models.BooleanField(default = False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['Complete_Name','Department','Role','is_member','is_hod','is_director']
    
    objects = CustomUserManager()
    
    def __str__(self):
        return str(self.email)

# class Person(models.Model):
#     id = models.AutoField(primary_key=True)
#     email = models.IntegerField(unique = True,null = False)
#     Complete_Name= models.CharField(max_length = 100)
#     Department = models.CharField(max_length = 100)
#     Role = models.CharField(max_length =100)
#     password = models.CharField(max_length = 100,default='tatamotors')
    
#     class Meta: 
#         verbose_name = 'Person'
#         verbose_name_plural = 'Persons'
    
#     def __str__(self):
#         return self.Complete_Name  
    

# class SuperV(models.Model):
#     email = models.IntegerField(primary_key = True,null= False)
#     Complete_Name= models.CharField(max_length = 100)
#     Department = models.CharField(max_length = 100)
#     Role = models.CharField(max_length =100)
#     password = models.CharField(max_length = 100,default='tatamotors')

#     class Meta: 
#         verbose_name = 'hod'
#         verbose_name_plural = 'hods'
        
#     def __str__(self):
#         return self.Complete_Name
    

