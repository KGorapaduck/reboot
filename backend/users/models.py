from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class User(AbstractUser):
    class Role(models.TextChoices):
        STUDENT = 'STUDENT', 'Student'
        INSTRUCTOR = 'INSTRUCTOR', 'Instructor'
        ADMIN = 'ADMIN', 'Admin'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nickname = models.CharField(max_length=50, blank=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.STUDENT)
    
    # 이메일은 선택사항이지만 고유해야 함 (옵션)
    email = models.EmailField(unique=True, blank=True, null=True)
    
    # USERNAME_FIELD = 'username' (기본값)
    REQUIRED_FIELDS = ['email', 'nickname']

    def __str__(self):
        return self.username

class UserProfile(models.Model):
    class CareerGoal(models.TextChoices):
        JOB_SEEKER = 'JOB_SEEKER', 'Job Seeker'
        ENTREPRENEUR = 'ENTREPRENEUR', 'Entrepreneur'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    career_goal = models.CharField(max_length=20, choices=CareerGoal.choices, default=CareerGoal.JOB_SEEKER)
    preferences = models.JSONField(default=dict, blank=True)  # 학습 스타일, 관심사 등
    portfolio_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.email}'s Profile"
