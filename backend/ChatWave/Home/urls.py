from django.urls import path
from .views import *

urlpatterns = [
   path('', homePageLogic, name="home")
]