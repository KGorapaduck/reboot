from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CurriculumViewSet, DashboardDataView

router = DefaultRouter()
router.register(r'curriculums', CurriculumViewSet, basename='curriculum')

urlpatterns = [
    path('dashboard/', DashboardDataView.as_view(), name='dashboard-data'),
    path('', include(router.urls)),
]
