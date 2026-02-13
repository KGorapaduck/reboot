from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet
from lectures.views import CourseViewSet, LectureViewSet, QuizViewSet
from ai_tutor.views import LectureNoteViewSet, AIChatSessionViewSet
from analytics.views import CurriculumViewSet, DashboardDataView
from assets.views import PortfolioViewSet, SkillBlockViewSet
from career.views import MockInterviewSessionViewSet, InterviewPersonaViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'lectures', LectureViewSet)
router.register(r'quizzes', QuizViewSet)
router.register(r'lecture-notes', LectureNoteViewSet, basename='lecture-note')
router.register(r'chat-sessions', AIChatSessionViewSet, basename='chat-session')
router.register(r'curriculums', CurriculumViewSet, basename='curriculum')
router.register(r'portfolios', PortfolioViewSet, basename='portfolio')
router.register(r'skill-blocks', SkillBlockViewSet)
router.register(r'interviews', MockInterviewSessionViewSet, basename='interview')
router.register(r'personas', InterviewPersonaViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/dashboard/', DashboardDataView.as_view(), name='dashboard-data'),
    path('api/', include(router.urls)),
]
