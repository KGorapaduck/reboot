from django.db import models
from django.conf import settings
import uuid
from pgvector.django import VectorField

class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50) # Frontend, Backend etc.
    instructor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='courses')
    created_at = models.DateTimeField(auto_now_add=True)
    cohort_analytics = models.JSONField(default=dict, blank=True, help_text="Cached average stats for the course cohort")

    def __str__(self):
        return self.title

class Lecture(models.Model):
    class AIStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        PROCESSING = 'PROCESSING', 'Processing'
        COMPLETED = 'COMPLETED', 'Completed'
        FAILED = 'FAILED', 'Failed'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lectures')
    title = models.CharField(max_length=200)
    video_url = models.URLField()
    duration = models.IntegerField(null=True, blank=True, help_text="Duration in seconds")
    order_index = models.IntegerField(default=0)
    
    # AI Processing Fields
    ai_status = models.CharField(max_length=20, choices=AIStatus.choices, default=AIStatus.PENDING)
    processing_error = models.TextField(blank=True, null=True)
    original_script = models.TextField(blank=True, help_text="Whisper STT result")
    embedding = VectorField(dimensions=1536, blank=True, null=True) # OpenAI embedding dimension
    
    # New JSON Fields for Advanced Features
    script_segments = models.JSONField(default=list, blank=True, help_text="List of script segments for pinpoint search")
    checkpoints = models.JSONField(default=list, blank=True, help_text="List of checkpoints/quizzes")
    supplemental_materials = models.JSONField(default=list, blank=True, help_text="Conditional supplemental materials")
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order_index']

    def __str__(self):
        return f"[{self.course.title}] {self.title}"

class Quiz(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name='quizzes')
    question = models.TextField()
    options = models.JSONField(help_text="JSON list of options")
    correct_answer = models.IntegerField(help_text="Index of the correct option")
    explanation = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Quiz for {self.lecture.title}"

class QuizAttempt(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='quiz_attempts')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    is_correct = models.BooleanField()
    solved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.quiz} ({'Correct' if self.is_correct else 'Wrong'})"
