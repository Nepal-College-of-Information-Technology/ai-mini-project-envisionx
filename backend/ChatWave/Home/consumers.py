import json
from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from .models import *
from django.template.loader import render_to_string
from asgiref.sync import async_to_sync
import re

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        self.chatroom_name = self.scope['url_route']['kwargs']['chatroom_name']
        self.chatroom = get_object_or_404(ChatRoom, room_name=self.chatroom_name)

        self.group_name = self.get_group_name(self.chatroom_name)


        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_datajson = json.loads(text_data)
        message = text_datajson['body']

        msg = ChatRoomMessages.objects.create(
            body=message,
            author=self.user,
            room=self.chatroom
        )

        context = {
            'message': msg,
        }
        html = render_to_string('partials/chat_message_p.html', context=context)

        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type': 'chat_message',
                'message': html
            }
        )

  
    def chat_message(self, event):
        message = event['message']

       
        self.send(text_data=message)

    @staticmethod
    def get_group_name(chatroom_name):
        sanitized_name = re.sub(r'[^a-zA-Z0-9_\-.]', '', chatroom_name)
        return f'chatroom_{sanitized_name[:95]}' 

