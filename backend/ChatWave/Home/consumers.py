import json
from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from .models import ChatRoom, ChatRoomMessages
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
        
        # Add and update online users
        if self.user not in self.chatroom.user_online.all():
            self.chatroom.user_online.add(self.user)
            self.update_online_count()

        self.accept()

    def disconnect(self, close_code):
        # Remove and update online users
        if self.user in self.chatroom.user_online.all():
            self.chatroom.user_online.remove(self.user)
            self.update_online_count()

        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['body']

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

    def update_online_count(self):
        online_count = self.chatroom.user_online.count()
        event = {
            'type': 'online_count_handler',
            'online_count': online_count,
        }
        async_to_sync(self.channel_layer.group_send)(self.group_name, event)

    def online_count_handler(self, event):
        online_count = event['online_count']
        html = render_to_string('partials/online_count.html', {'online_count': online_count})
        self.send(text_data=html)
