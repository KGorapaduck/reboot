from django.db import models
from django.conf import settings
from lectures.models import Course, Lecture
import uuid

class Curriculum(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Active'
        COMPLETED = 'COMPLETED', 'Completed'
        DROPPED = 'DROPPED', 'Dropped'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='curriculums')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='active_curriculums')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    start_date = models.DateTimeField(auto_now_add=True)
    target_date = models.DateTimeField(help_text="Goal date for completion")
    retention_metrics = models.JSONField(default=dict, blank=True, help_text="Dropout risk analysis data")

    def __str__(self):
        return f"{self.user} - {self.course} ({self.status})"

class CurriculumItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE, related_name='items')
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name='curriculum_items')
    order_index = models.IntegerField(help_text="Dynamically adjustable order")
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # New JSON Fields for detailed tracking
    learning_status = models.JSONField(default=dict, blank=True, help_text="Micro-tracking of watch history and checkpoints")
    reflection_data = models.JSONField(default=dict, blank=True, help_text="User reflections and AI feedback")

    class Meta:
        ordering = ['order_index']

    def __str__(self):
        return f"{self.curriculum} - {self.lecture} [{'V' if self.is_completed else ' '}]"

class ReroutingLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE, related_name='rerouting_logs')
    reason = models.CharField(max_length=100, help_text="Reason for rerouting (e.g., Fell behind)")
    old_path = models.JSONField(help_text="List of Lecture IDs before change")
    new_path = models.JSONField(help_text="List of Lecture IDs after change (Fast Track)")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reroute for {self.curriculum} at {self.created_at}"
