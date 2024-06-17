from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager

class CustomUser(AbstractUser):
    username = models.CharField(_("Username"), max_length=100, unique=True)
    profile_picture = models.ImageField(_("Profile"), blank=True, null=True)
    email = models.EmailField(_("Email"), unique=True)
    phone_number = models.CharField(_("Phone Number"),max_length=15, blank=True, null=True)
    about = models.TextField(_("About"), blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # Add 'username' to REQUIRED_FIELDS

    objects = CustomUserManager()

    def __str__(self):
        return self.username
