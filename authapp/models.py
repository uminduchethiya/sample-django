from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    first_name=models.CharField(max_length=10)
    last_name=models.CharField(max_length=10)
    email=models.EmailField(unique=True)
    phone_number=models.CharField(max_length=20,blank=True,null=True)
    
    class Roles(models.TextChoices):
        Admin='admin','Admin'
        Customer='customer','Customer'
        
    role = models.CharField(max_length=10, choices=Roles.choices, default=Roles.Customer)
    
    REQUIRED_FIELDS=['email','first_name','last_name']
    
    def __str__(self):
        return f"{self.username} ({self.role})"

