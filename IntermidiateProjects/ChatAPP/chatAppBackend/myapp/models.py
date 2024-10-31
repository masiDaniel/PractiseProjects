from django.db import models
from django.contrib.auth.models import  User

# Create your models here.
class ChatRoom(models.Model):
    name = models.CharField(max_length=100, unique=True)
    participants = models.ManyToManyField(User, related_name="chat_rooms")

    def __str__(self):
        return self.name


class ChatMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name="received_messages")
    room = models.ForeignKey(ChatRoom, null=True, blank=True, on_delete=models.CASCADE, related_name="messages")
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.room:
            return f"{self.sender} in {self.room.name} at {self.timestamp}"
        return f"{self.sender} to {self.receiver} at {self.timestamp}"