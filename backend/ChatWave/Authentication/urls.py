from django.urls import path
from .views import *

urlpatterns = [
    path('register', registerLogic, name = 'register'),
    path('login', loginLogic, name='login')
]