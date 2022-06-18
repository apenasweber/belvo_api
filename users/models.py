from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

class User(AbstractBaseUser,PermissionsMixin):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    

class Transaction(models.Model):
    reference = models.CharField(max_length=255, unique=True)
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)