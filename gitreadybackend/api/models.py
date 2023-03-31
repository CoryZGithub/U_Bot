from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    USER = 'user'
    ASSISTANT = 'assistant'
    SYSTEM = 'system'

    ROLE_CHOICES = [
        (USER, 'User'),
        (ASSISTANT, 'Assistant'),
        (SYSTEM, 'System'),
    ]
    content = models.TextField()
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['timestamp']
    
    def to_json(self):
        return {
            'role': self.role,
            'content': self.content,
        }
    
    