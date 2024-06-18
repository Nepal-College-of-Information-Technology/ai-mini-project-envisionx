from django.db import models

class Message(models.Model):
    text = models.textField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    
    def __str__(self):
        return self.text
    
    