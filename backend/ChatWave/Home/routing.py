from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('home/ws/chat/<str:chatroom_name>/', consumers.ChatConsumer.as_asgi()),
]
