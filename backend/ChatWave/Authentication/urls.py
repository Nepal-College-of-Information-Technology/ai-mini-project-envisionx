from django.urls import path
from .views import *


urlpatterns = [
    path('register', registerLogic, name = 'register'),
    path('login', loginLogic, name='login'),
#    path('activate/<uidb64>/<token>',activate, name='activate'),
]