from rest_framework import serializers
from .models import LectureNote, AIChatSession, AIChatMessage

class LectureNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = LectureNote
        fields = ['id', 'lecture', 'user', 'summary', 'keywords', 'created_at']
        read_only_fields = ['summary', 'keywords', 'created_at']

class AIChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIChatMessage
        fields = ['id', 'sender', 'message', 'created_at']

class AIChatSessionSerializer(serializers.ModelSerializer):
    messages = AIChatMessageSerializer(many=True, read_only=True)

    class Meta:
        model = AIChatSession
        fields = ['id', 'user', 'lecture', 'start_time', 'messages']
        read_only_fields = ['start_time', 'messages']
