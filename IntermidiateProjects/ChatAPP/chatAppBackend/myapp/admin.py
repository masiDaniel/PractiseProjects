from django.contrib import admin

from myapp.models import ChatRoom, ChatMessage

# Register your models here.
admin.site.register(ChatRoom)
admin.site.register(ChatMessage)