import os
import django
import sys

# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from ai_tutor.stt_service import STTService

def test_segmented_stt(url):
    print(f"Starting Segmented Diagnostic for: {url}")
    try:
        # We expect it to yield segments chunk by chunk
        count = 0
        for segment in STTService.process_video(url):
            count += 1
            print(f"[{count}] Received segment at {segment['start']:.2f}s: {segment['content'][:50]}...")
            if count >= 10: break # Just a few for verification
        print(f"Diagnostic segment testing complete. Total received in this test: {count}")
    except Exception as e:
        print(f"DIAGNOSTIC FAILED: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_url = "https://www.youtube.com/watch?v=DWO4DoRiI60"
    test_segmented_stt(test_url)
