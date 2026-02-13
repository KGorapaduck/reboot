import openai
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class OpenAIService:
    @staticmethod
    def get_client():
        return openai.OpenAI(api_key=settings.OPENAI_API_KEY)

    @staticmethod
    def transcribe_audio(file_path):
        """
        Transcribes audio file using Whisper model.
        """
        client = OpenAIService.get_client()
        try:
            with open(file_path, "rb") as audio_file:
                transcription = client.audio.transcriptions.create(
                    model="Faster-Whisper",
                    file=audio_file
                )
            return transcription.text
        except Exception as e:
            logger.error(f"Error transcribing audio: {e}")
            return None

    @staticmethod
    def get_embedding(text):
        """
        Generates embedding for text using text-embedding-3-small (or ada-002).
        """
        client = OpenAIService.get_client()
        try:
            response = client.embeddings.create(
                input=text,
                model="text-embedding-3-small"
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            return None

    @staticmethod
    def chat_completion(messages, model="gpt-4o"):
        """
        Generates response using GPT-4o model.
        """
        client = OpenAIService.get_client()
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error generating chat completion: {e}")
            return None
