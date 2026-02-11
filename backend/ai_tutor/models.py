from django.db import models
from django.conf import settings
from lectures.models import Lecture
import uuid

class LectureNote(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lecture = models.OneToOneField(Lecture, on_delete=models.CASCADE, related_name='note')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='custom_notes', help_text="Null for default AI note, set for user custom note")
    summary = models.TextField(help_text="AI generated summary")
    keywords = models.JSONField(default=list, help_text="Extracted keywords")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Note for {self.lecture.title}"

class AIChatSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_sessions')
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name='chat_sessions', help_text="Context for the chat")
    start_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat Session: {self.user} - {self.lecture}"

class AIChatMessage(models.Model):
    class Sender(models.TextChoices):
        USER = 'USER', 'User'
        AI = 'AI', 'AI'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(AIChatSession, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=10, choices=Sender.choices)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.sender}] {self.message[:50]}..."
