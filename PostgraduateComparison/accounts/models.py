from django.db import models
from .managers import CustomUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
# Create your models here.

class CustomUser(AbstractUser):
    username = models.CharField(max_length=255)
    email = models.EmailField(_("email address"), unique=True)
    is_verified = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    
    @property
    def is_admin(self):
        return self.is_employee

class Student(models.Model):
    user = models.OneToOneField(CustomUser, related_name='student', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username

class Employee(models.Model):
    user = models.OneToOneField(CustomUser, related_name='employer', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username

