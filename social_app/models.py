from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True, verbose_name='تاریخ تولد')
    bio = models.TextField(blank=True, null=True, verbose_name='بایو')
    photo = models.ImageField(upload_to='account_images/', blank=True, null=True, verbose_name='عکس پروفایل')
    job = models.CharField(max_length=250, blank=True, null=True, verbose_name='شغل')
    phone = models.CharField(max_length=11, blank=True, null=True, verbose_name='شماره تلفن')
