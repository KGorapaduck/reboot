import os
import yt_dlp
from django.conf import settings
from core.services import OpenAIService

class STTService:
    @staticmethod
    def download_audio(youtube_url, base_path=None):
        """
        Download audio from YouTube URL using yt-dlp in a unique temp directory.
        Returns (audio_path, temp_dir).
        """
        import uuid
        if base_path is None:
            base_path = os.path.join(settings.BASE_DIR, "temp_downloads")
        
        # Create a unique directory for this specific download
        temp_dir = os.path.join(base_path, str(uuid.uuid4()))
        os.makedirs(temp_dir, exist_ok=True)

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': f'{temp_dir}/%(id)s.%(ext)s',
            'quiet': True,
            'no_warnings': True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(youtube_url, download=True)
                file_id = info['id']
                audio_path = os.path.join(temp_dir, f"{file_id}.mp3")
                return audio_path, temp_dir
        except Exception as e:
            print(f"Error downloading audio: {e}")
            return None, temp_dir

    @staticmethod
    def transcribe_audio(audio_path):
        """
        Transcribe audio file using OpenAI Whisper API.
        Returns the transcription object with segments.
        """
        if not audio_path or not os.path.exists(audio_path):
            return None
        
        try:
            client = OpenAIService.get_client()
            print(f"STT: Transcribing {audio_path}...")
            if not os.path.exists(audio_path) or os.path.getsize(audio_path) == 0:
                print(f"STT: Skip empty or missing file {audio_path}")
                return None
            # Reduced file size or chunks might be needed for very long videos, 
            # but Whisper API handles up to 25MB.
            with open(audio_path, "rb") as audio_file:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1", 
                    file=audio_file,
                    response_format="verbose_json",
                    timestamp_granularities=["segment"]
                )
            print(f"STT: Transcription successful for {audio_path}")
            return transcript
        except Exception as e:
            print(f"STT Error transcribing audio: {e}")
            return None

    @staticmethod
    def correct_segments(segments):
        """
        Use GPT-4o to correct typos and improve natural language in segments,
        keeping the structure.
        """
        if not segments:
            return []
        
        # Format segments for GPT
        text_to_correct = "\n".join([f"[{i}] {seg['content']}" for i, seg in enumerate(segments)])
        
        prompt = f"""
        당신은 한국어 STT(영상 자막) 교정 전문가입니다. 
        다음은 Whisper AI로 추출한 가공되지 않은 자막 데이터입니다.
        
        [지침]
        1. 문맥을 고려하여 오타, 맞춤법, 띄어쓰기를 수정하세요.
        2. 전문 용어나 고유 명사(예: 프로그래밍 언어, 라이브러리 이름 등)가 오타로 인식된 경우 올바르게 수정하세요.
        3. 문장의 의미를 해치지 않는 선에서 자연스러운 구어체로 다듬으세요.
        4. 반드시 제공된 번호 형식을 유지하며, 번호 하나당 수정된 문장 하나씩만 출력하세요.
        
        [대상 데이터]
        {text_to_correct}
        
        [출력 예시]
        [0] 안녕하세요, 오늘은 뷰제이에스에 대해 배워보겠습니다.
        [1] 먼저 프로젝트를 생성해볼까요?
        """
        
        messages = [
            {"role": "system", "content": "당신은 한국어 자막 교정 전문가입니다."},
            {"role": "user", "content": prompt}
        ]
        
        try:
            corrected_text = OpenAIService.chat_completion(messages)
            if not corrected_text:
                return segments
                
            corrected_lines = corrected_text.strip().split('\n')
            new_segments = []
            for line in corrected_lines:
                import re
                match = re.match(r'\[(\d+)\]\s*(.*)', line.strip())
                if match:
                    idx = int(match.group(1))
                    if idx < len(segments):
                        new_segments.append({
                            "start": segments[idx]["start"],
                            "end": segments[idx]["end"],
                            "content": match.group(2).strip()
                        })
            
            # If parsing failed or mismatch, return original to be safe
            return new_segments if len(new_segments) == len(segments) else segments
        except Exception as e:
            print(f"STT: Error during typo correction: {e}")
            return segments

    @staticmethod
    def process_video(youtube_url):
        """
        Orchestrate the download and transcription process.
        Splits audio into 60s chunks for segmented (near real-time) processing.
        Returns a generator that yields segments incrementally.
        """
        import shutil
        import subprocess
        import glob
        
        print(f"STT: Processing video {youtube_url} in segments")
        audio_path, temp_dir = STTService.download_audio(youtube_url)
        
        try:
            if not audio_path or not os.path.exists(audio_path):
                print("STT: Failed to download audio")
                return
                
            # Split the audio into 60s chunks using ffmpeg
            # %03d.mp3 creates 000.mp3, 001.mp3, etc.
            chunk_pattern = os.path.join(temp_dir, "chunk_%03d.mp3")
            print(f"STT: Splitting {audio_path} into 60s chunks...")
            
            # -f segment -segment_time 60 splits into 60s parts
            split_cmd = [
                'ffmpeg', '-i', audio_path,
                '-f', 'segment', '-segment_time', '60',
                '-c', 'copy', chunk_pattern
            ]
            
            subprocess.run(split_cmd, capture_output=True, check=True)
            
            chunks = sorted(glob.glob(os.path.join(temp_dir, "chunk_*.mp3")))
            print(f"STT: Created {len(chunks)} chunks for processing")
            
            for i, chunk_path in enumerate(chunks):
                offset = i * 60.0
                print(f"STT: Transcribing chunk {i} (starts at {offset}s)")
                
                transcript = STTService.transcribe_audio(chunk_path)
                if not transcript:
                    continue
                    
                chunk_segments = []
                if hasattr(transcript, 'segments') and transcript.segments:
                    for seg in transcript.segments:
                        try:
                            start = seg.start if hasattr(seg, 'start') else seg.get('start', 0)
                            end = seg.end if hasattr(seg, 'end') else seg.get('end', 0)
                            text = seg.text if hasattr(seg, 'text') else seg.get('text', '')
                            
                            chunk_segments.append({
                                "start": start + offset,
                                "end": end + offset,
                                "content": text.strip()
                            })
                        except Exception as e:
                            print(f"STT: Error parsing segment in chunk {i}: {e}")
                else:
                    # Fallback for small chunks
                    text = transcript.text if hasattr(transcript, 'text') else getattr(transcript, 'text', '')
                    if text.strip():
                        chunk_segments.append({"start": offset, "end": offset + 60, "content": text.strip()})
                
                # Apply AI correction to the chunk
                if chunk_segments:
                    print(f"STT: Correcting typos for chunk {i}...")
                    corrected_segments = STTService.correct_segments(chunk_segments)
                    for seg in corrected_segments:
                        yield seg

        except Exception as e:
            print(f"STT: Critical error during segmented processing: {e}")
        finally:
            # Cleanup the entire unique temp directory
            if temp_dir and os.path.exists(temp_dir):
                try:
                    shutil.rmtree(temp_dir)
                    print(f"STT: Cleaned up {temp_dir}")
                except Exception as e:
                    print(f"STT: Cleanup failed for {temp_dir}: {e}")
