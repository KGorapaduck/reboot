from django.db import models
from django.conf import settings
from lectures.models import Course, Quiz
import uuid

class SkillBlock(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='skill_blocks')
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    criteria = models.TextField(help_text="Logic for earning this skill")
    
    def __str__(self):
        return self.name

class UserSkill(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='skills')
    skill_block = models.ForeignKey(SkillBlock, on_delete=models.CASCADE, related_name='awarded_users')
    acquired_at = models.DateTimeField(auto_now_add=True)
    verification_source = models.CharField(max_length=100, help_text="Source ID (e.g., Quiz:123)")

    def __str__(self):
        return f"{self.user} - {self.skill_block}"

class Portfolio(models.Model):
    class Type(models.TextChoices):
        RESUME = 'RESUME', 'Resume'
        BUSINESS_PLAN = 'BUSINESS_PLAN', 'Business Plan'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='portfolios')
    title = models.CharField(max_length=200)
    type = models.CharField(max_length=20, choices=Type.choices)
    sections = models.JSONField(default=dict, help_text="Structured data for sections")
    compiled_markdown = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.title} ({self.type})"

class PortfolioProject(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='projects')
    skill_block = models.ForeignKey(SkillBlock, on_delete=models.SET_NULL, null=True, blank=True, related_name='portfolio_projects')
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name
