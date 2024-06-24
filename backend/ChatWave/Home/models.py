from django.db import models
# from django.contrib.auth.models import User
from django.conf import settings

class ChatRoom(models.Model):
    room_name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.room_name
    


class ChatRoomMessages(models.Model):
    room = models.ForeignKey(ChatRoom, related_name='messages', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.room} : {self.author.username} : {self.body}'
    

    class Meta:
        ordering = ['-created']
    
    