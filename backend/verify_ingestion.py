
import os
import django
from unittest.mock import MagicMock, patch

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from lectures.models import Lecture, Course
from ai_tutor.stt_service import STTService
from ai_tutor.summary_service import SummaryService

def test_pipeline():
    print("Testing Ingestion Pipeline Logic...")
    
    # 1. Setup Mock Data
    course, _ = Course.objects.get_or_create(title="Test Course")
    lecture, _ = Lecture.objects.get_or_create(course=course, title="Test Lecture", defaults={
        "video_url": "https://youtu.be/test",
        "duration": 100
    })

    # 2. Mock External Services
    with patch('ai_tutor.stt_service.STTService.download_audio', return_value="dummy.mp3") as mock_download, \
         patch('ai_tutor.stt_service.STTService.transcribe_audio') as mock_transcribe, \
         patch('ai_tutor.summary_service.OpenAIService.chat_completion', return_value="## Mock Summary") as mock_summary:
        
        # Mock Transcription Result
        mock_transcribe.return_value = MagicMock(segments=[
            {"start": 0, "end": 10, "text": "Hello world"},
            {"start": 10, "end": 20, "text": "This is a test"}
        ])

        print("- Simulating Video Processing...")
        
        # 3. Simulate Logic from View
        lecture.ai_status = Lecture.AIStatus.PROCESSING
        lecture.save()

        # STT
        segments = STTService.process_video(lecture.video_url)
        lecture.script_segments = segments
        lecture.save()
        print(f"  > STT Segments: {len(segments)}")

        # Summary
        summary = SummaryService.summarize_script(segments)
        lecture.original_script = summary
        lecture.ai_status = Lecture.AIStatus.COMPLETED
        lecture.save()
        print(f"  > Summary: {summary}")

    # 4. Verify DB
    refreshed_lecture = Lecture.objects.get(id=lecture.id)
    assert refreshed_lecture.ai_status == Lecture.AIStatus.COMPLETED
    assert len(refreshed_lecture.script_segments) == 2
    assert refreshed_lecture.original_script == "## Mock Summary"
    
    print("Pipeline Verification Passed! ✅")

if __name__ == "__main__":
    test_pipeline()
