from django.db import models
from django.conf import settings
from assets.models import Portfolio
import uuid

class InterviewPersona(models.Model):
    class Role(models.TextChoices):
        TECH_LEAD = 'TECH_LEAD', 'Tech Lead'
        HR = 'HR', 'HR Manager'
        VC = 'VC', 'VC Investor'
        PEER = 'PEER', 'Peer Developer'
        CUSTOMER = 'CUSTOMER', 'Potential Customer'
        CTO = 'CTO', 'CTO'

    class Difficulty(models.TextChoices):
        EASY = 'EASY', 'Easy'
        NORMAL = 'NORMAL', 'Normal'
        HARD = 'HARD', 'Hard'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=Role.choices)
    system_prompt = models.TextField(help_text="Prompt for AI Persona")
    difficulty = models.CharField(max_length=10, choices=Difficulty.choices)

    def __str__(self):
        return f"{self.name} ({self.role})"

class MockInterviewSession(models.Model):
    class Status(models.TextChoices):
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        COMPLETED = 'COMPLETED', 'Completed'
        TIMEOUT = 'TIMEOUT', 'Timeout'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='interview_sessions')
    persona = models.ForeignKey(InterviewPersona, on_delete=models.CASCADE, related_name='sessions')
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='interviews')
    
    target_question_count = models.IntegerField(default=5, help_text="Target questions for auto-termination")
    time_limit_seconds = models.IntegerField(default=600, help_text="Time limit in seconds")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.IN_PROGRESS)
    
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    score = models.IntegerField(null=True, blank=True)
    feedback_summary = models.TextField(blank=True)
    evaluation_detail = models.JSONField(default=dict, blank=True, help_text="Detailed evaluation results")

    def __str__(self):
        return f"Interview with {self.persona.name} on {self.start_time}"

class MockInterviewMessage(models.Model):
    class Sender(models.TextChoices):
        USER = 'USER', 'User'
        AI = 'AI', 'AI'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(MockInterviewSession, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=10, choices=Sender.choices)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.sender}] {self.content[:50]}..."
