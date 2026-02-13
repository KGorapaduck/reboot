from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Curriculum, CurriculumItem
from .serializers import CurriculumDetailSerializer

class CurriculumViewSet(viewsets.ModelViewSet):
    serializer_class = CurriculumDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Curriculum.objects.filter(user=self.request.user)

    @action(detail=True, methods=['post'])
    def complete_lecture(self, request, pk=None):
        lecture_id = request.data.get('lecture_id')
        curriculum = self.get_object()
        item = CurriculumItem.objects.get(curriculum=curriculum, lecture_id=lecture_id)
        
        item.is_completed = True
        item.save()
        
        return Response({'status': 'lecture marked complete'})

from rest_framework.views import APIView
from users.models import User
from lectures.models import Lecture
from assets.models import UserSkill
from django.db.models import Sum

class DashboardDataView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        
        # 1. User Info & Profile
        try:
            profile = user.profile
            career_goal = profile.career_goal
        except:
            career_goal = "NOT_SET"

        user_data = {
            "username": user.username,
            "nickname": user.nickname,
            "career_goal": career_goal
        }

        # 2. Statistics
        # Calculate total duration of completed lectures
        completed_items = CurriculumItem.objects.filter(curriculum__user=user, is_completed=True)
        # Assuming we can sum up lecture durations. 
        # For simplicity, let's count completed items * average duration or just fetch lectures.
        total_seconds = 0
        for item in completed_items:
            total_seconds += item.lecture.duration
        
        total_study_time = total_seconds // 60 # minutes
        completed_lectures_count = completed_items.count()
        earned_skills_count = UserSkill.objects.filter(user=user).count()
        
        stats = {
            "total_study_time": total_study_time,
            "completed_lectures_count": completed_lectures_count,
            "earned_skills_count": earned_skills_count
        }

        # 3. Active Curriculums
        active_curriculums_qs = Curriculum.objects.filter(user=user, status='ACTIVE')
        curriculums_data = []
        for curr in active_curriculums_qs:
            # Calculate progress
            total_items = curr.items.count()
            done_items = curr.items.filter(is_completed=True).count()
            progress = int((done_items / total_items) * 100) if total_items > 0 else 0
            
            curriculums_data.append({
                "id": curr.id,
                "course_id": curr.course.id,
                "course_title": curr.course.title,
                "status": curr.status,
                "target_date": curr.target_date,
                "progress": progress,
                "cohort_analytics": curr.course.cohort_analytics,
                "retention_metrics": curr.retention_metrics
            })

        # 4. Recent Activity (Latest 3 completed or in-progress items)
        # In a real app, we might use a separate AccessLog table. 
        # Here we use CurriculumItem updated_at if we had one, or just pick from active curriculums.
        # For now, let's pick the last 3 completed items.
        recent_items = CurriculumItem.objects.filter(curriculum__user=user, is_completed=True).order_by('-completed_at')[:3]
        recent_lectures = []
        for item in recent_items:
            recent_lectures.append({
                "id": item.lecture.id,
                "course_name": item.curriculum.course.title,
                "title": item.lecture.title,
                "last_accessed": item.completed_at
            })

        return Response({
            "user": user_data,
            "stats": stats,
            "curriculums": curriculums_data,
            "recent_lectures": recent_lectures
        })
