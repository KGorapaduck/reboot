from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Course, Lecture, Quiz, QuizAttempt
from .serializers import (
    CourseListSerializer, CourseDetailSerializer, 
    LectureSerializer, QuizSerializer, QuizAttemptSerializer
)
import logging
import re
import threading

logger = logging.getLogger(__name__)

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

    # Removed background threading logic as it caused hangs with SQLite
    def _run_processing(self, lecture_id):
        # We fetch a fresh instance in the thread to avoid issues
        from lectures.models import Lecture
        from ai_tutor.stt_service import STTService
        from ai_tutor.summary_service import SummaryService
        import time

        try:
            lecture = Lecture.objects.get(id=lecture_id)
            lecture.ai_status = Lecture.AIStatus.PROCESSING
            lecture.script_segments = [] # Clear old if any
            lecture.save()

            logger.info(f"Background: Starting internal audio STT for {lecture.video_url}")
            
            # Incremental STT
            segments = []
            for segment in STTService.process_video(lecture.video_url):
                segments.append(segment)
                # Bulk update segments periodically to avoid too many writes
                # but frequent enough for "real-time" feel
                lecture.script_segments = segments
                lecture.save()
                logger.info(f"Background: Added segment for {lecture_id}")

            if not segments:
                raise Exception("STT yielded no segments")
            
            # Final summarization
            summary = SummaryService.summarize_script(segments)
            lecture.original_script = summary 
            lecture.ai_status = Lecture.AIStatus.COMPLETED
            lecture.save()
            logger.info(f"Background: AI processing completed for {lecture_id}")

        except Exception as e:
            logger.error(f"Background: AI Processing failed for {lecture_id}: {str(e)}")
            try:
                lecture = Lecture.objects.get(id=lecture_id)
                lecture.ai_status = Lecture.AIStatus.FAILED
                lecture.processing_error = str(e)
                lecture.save()
            except:
                pass

    def _trigger_processing(self, lecture):
        # Start background thread for incremental updates
        thread = threading.Thread(target=self._run_processing, args=(lecture.id,))
        thread.daemon = True
        thread.start()

    def _extract_youtube_id(self, url):
        patterns = [
            r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
            r'youtu\.be\/([0-9A-Za-z_-]{11})',
            r'embed\/([0-9A-Za-z_-]{11})'
        ]
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None

    @action(detail=False, methods=['post'])
    def get_by_url(self, request):
        video_url = request.data.get('video_url')
        logger.info(f"Classroom API: get_by_url request received for {video_url}")
        
        if not video_url:
             return Response({'error': 'No video URL provided'}, status=400)
        
        video_id = self._extract_youtube_id(video_url)
        if not video_id:
             logger.warning(f"Classroom API: Invalid YouTube URL provided: {video_url}")
             # Still try to filter by exact match just in case, or return error
             
        # Try to find by video_id in URL or exact match
        lecture = Lecture.objects.filter(video_url__icontains=video_id if video_id else video_url).first()
        
        if not lecture:
            logger.info(f"Classroom API: Lecture not found for {video_id}. Creating new one.")
            course = Course.objects.first()
            if not course:
                logger.info("Classroom API: No courses found. Creating default course.")
                course = Course.objects.create(
                    title="기본 강의 보관함",
                    instructor=request.user,
                    description="자동 생성된 유튜브 강의실입니다."
                )
            
            lecture = Lecture.objects.create(
                course=course,
                title="새로운 유튜브 강의",
                video_url=video_url,
                ai_status=Lecture.AIStatus.PENDING
            )
            # Trigger ONLY if new or pending
            self._trigger_processing(lecture)
        else:
            logger.info(f"Classroom API: Lecture found (ID: {lecture.id})")
            if lecture.ai_status in [Lecture.AIStatus.PENDING, Lecture.AIStatus.FAILED]:
                self._trigger_processing(lecture)
        
        # Ensure it returns immediately
        serializer = self.get_serializer(lecture)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def transcribe_segment(self, request, pk=None):
        lecture = self.get_object()
        audio_file = request.FILES.get('audio')
        if not audio_file:
            return Response({'error': 'No audio file provided'}, status=400)
            
        try:
            from core.services import OpenAIService
            import tempfile
            import os
            
            # Save temporary file
            with tempfile.NamedTemporaryFile(suffix='.webm', delete=False) as tmp:
                for chunk in audio_file.chunks():
                    tmp.write(chunk)
                tmp_path = tmp.name
                
            try:
                text = OpenAIService.transcribe_audio(tmp_path)
                return Response({'text': text})
            finally:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
        except Exception as e:
            return Response({'error': str(e)}, status=500)

    @action(detail=True, methods=['post'])
    def process_video(self, request, pk=None):
        lecture = self.get_object()
        self._trigger_processing(lecture)
        return Response({'status': 'Processing triggered'})

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
