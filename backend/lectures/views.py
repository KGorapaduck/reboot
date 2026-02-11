from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Course, Lecture, Quiz, QuizAttempt
from .serializers import (
    CourseListSerializer, CourseDetailSerializer, 
    LectureSerializer, QuizSerializer, QuizAttemptSerializer
)

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    # serializer_class handled in get_serializer_class
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'list':
            return CourseListSerializer
        return CourseDetailSerializer

class LectureViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        # Mark lecture as completed in Analytics (CurriculumItem)
        # This will be implemented when integrating with Analytics
        return Response({'status': 'completed'})

class QuizViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        quiz = self.get_object()
        selected_option = request.data.get('selected_option')
        
        if selected_option is None:
            return Response({'error': 'No option selected'}, status=status.HTTP_400_BAD_REQUEST)
        
        is_correct = (selected_option == quiz.correct_answer)
        
        attempt = QuizAttempt.objects.create(
            user=request.user,
            quiz=quiz,
            is_correct=is_correct
        )
        
        return Response({
            'is_correct': is_correct,
            'correct_answer': quiz.correct_answer,
            'explanation': quiz.explanation
        })
