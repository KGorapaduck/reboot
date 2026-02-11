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
        
        # Check overall progress and suggest rerouting if needed
        # self.check_progress(curriculum)
        
        return Response({'status': 'lecture marked complete'})
