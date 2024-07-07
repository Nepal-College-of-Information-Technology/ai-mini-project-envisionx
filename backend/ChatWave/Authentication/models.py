from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager

class CustomUser(AbstractUser):
    username = models.CharField(_("Username"), max_length=100, unique=True)
    email = models.EmailField(_("Email"), unique=True)

    USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = ['username']  

    objects = CustomUserManager()

    def __str__(self):
        return self.username
