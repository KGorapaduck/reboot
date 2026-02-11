from rest_framework import serializers
from .models import InterviewPersona, MockInterviewSession, MockInterviewMessage
from assets.serializers import PortfolioSerializer

class InterviewPersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewPersona
        fields = ['id', 'name', 'role', 'system_prompt', 'difficulty']

class MockInterviewMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MockInterviewMessage
        fields = ['id', 'sender', 'content', 'created_at']

class MockInterviewSessionSerializer(serializers.ModelSerializer):
    persona = InterviewPersonaSerializer(read_only=True)
    messages = MockInterviewMessageSerializer(many=True, read_only=True)
    portfolio_title = serializers.CharField(source='portfolio.title', read_only=True)

    class Meta:
        model = MockInterviewSession
        fields = ['id', 'user', 'persona', 'portfolio', 'portfolio_title', 
                  'target_question_count', 'time_limit_seconds', 'status', 
                  'start_time', 'end_time', 'score', 'feedback_summary', 'evaluation_detail', 'messages']
        read_only_fields = ['user', 'start_time', 'end_time', 'score', 'feedback_summary', 'evaluation_detail', 'messages']
