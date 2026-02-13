
import os
import django
import uuid
from datetime import timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from users.models import User, UserProfile
from lectures.models import Course, Lecture, Quiz
from analytics.models import Curriculum, CurriculumItem
from assets.models import SkillBlock, UserSkill

def run_seed():
    print("Seeding Dashboard Data...")

    # 1. Create User
    user, created = User.objects.get_or_create(username='student1', defaults={
        'email': 'student1@example.com', 
        'nickname': '열공러',
        'role': 'STUDENT'
    })
    if created:
        user.set_password('password123')
        user.save()
        UserProfile.objects.create(user=user, career_goal='JOB_SEEKER')
    print(f"User: {user.username}")

    # 2. Create Course & Lectures
    instructor, created = User.objects.get_or_create(username='instructor1', defaults={'role': 'INSTRUCTOR', 'email': 'instructor1@example.com', 'nickname': 'Dr. Code'})
    if created or instructor.password == "":
        instructor.set_password('password123')
        instructor.save()
    print(f"Instructor: {instructor.username} (password123)")
    
    course, created = Course.objects.get_or_create(title='Advanced React Patterns', defaults={
        'description': 'Master React with advanced patterns',
        'category': 'Frontend',
        'instructor': instructor,
        'cohort_analytics': {"avg_progress": 45.5, "avg_quiz_score": 78}
    })
    
    # Create lectures with checkpoints
    lectures_data = [
        ("Intro to Patterns", 300, []),
        ("HOC (Higher Order Components)", 600, [{
            "id": str(uuid.uuid4()), "time_point": 120, 
            "question": "HOC의 주요 목적은?", 
            "options": ["Code Reuse", "Styling", "Data Fetching"], "answer": 0
        }]),
        ("Render Props", 500, []),
        ("Custom Hooks", 600, []),
        ("Compound Components", 700, [])
    ]
    
    lectures = []
    for idx, (title, dur, cps) in enumerate(lectures_data):
        lec, _ = Lecture.objects.get_or_create(course=course, title=title, defaults={
            'video_url': 'https://www.youtube.com/watch?v=DWO4DoRiI60',
            'duration': dur,
            'order_index': idx,
            'checkpoints': cps,
            'script_segments': [{"start": 0, "end": 60, "content": f"{title} 시작입니다.", "keywords": ["Intro"]}]
        })
        lectures.append(lec)

    # 3. Create Curriculum
    curriculum, created = Curriculum.objects.get_or_create(user=user, course=course, defaults={
        'target_date': timezone.now() + timedelta(days=30),
        'retention_metrics': {
            "dropout_risk_score": 0.65, 
            "riskLevel": "medium", 
            "quiz_fail_streak": 1
        }
    })

    # 4. Create Curriculum Items & Progress
    for i, lec in enumerate(lectures):
        item, _ = CurriculumItem.objects.get_or_create(curriculum=curriculum, lecture=lec, defaults={
            'order_index': i
        })
        # Mark first 2 as complete
        if i < 2:
            item.is_completed = True
            item.completed_at = timezone.now() - timedelta(days=2-i)
            item.learning_status = {"watched_segments": [[0, lec.duration]]}
            item.save()

    # 5. Skills
    skill, _ = SkillBlock.objects.get_or_create(name='React Expert', defaults={
        'category': 'Frontend',
        'course': course,
        'criteria': 'Complete checkpoints'
    })
    UserSkill.objects.get_or_create(user=user, skill_block=skill, defaults={'verification_source': 'Quiz:123'})

    print("Seeding Complete!")

if __name__ == '__main__':
    run_seed()
