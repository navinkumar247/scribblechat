from django.db import models
from django.contrib.auth import get_user_model
from profiles.models import Relationship
User = get_user_model()

# Create your models here.
class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'author_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    relation  = models.ForeignKey(Relationship, on_delete=models.CASCADE, related_name='relation')
    

    def __str__(self):
        return self.author.username

    def last_30_messages(relation):
        return Message.objects.filter(relation=relation).order_by('-timestamp').all()[:30]

