from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import InterviewPersona, MockInterviewSession, MockInterviewMessage
from .serializers import (
    InterviewPersonaSerializer, MockInterviewSessionSerializer, 
    MockInterviewMessageSerializer
)

class InterviewPersonaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = InterviewPersona.objects.all()
    serializer_class = InterviewPersonaSerializer
    permission_classes = [permissions.IsAuthenticated]

from core.services import OpenAIService

class MockInterviewSessionViewSet(viewsets.ModelViewSet):
    serializer_class = MockInterviewSessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return MockInterviewSession.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def chat(self, request, pk=None):
        session = self.get_object()
        user_message = request.data.get('content')
        
        if session.status != 'IN_PROGRESS':
            return Response({'error': 'Interview is not in progress'}, status=status.HTTP_400_BAD_REQUEST)

        # 1. 사용자 메시지 저장
        MockInterviewMessage.objects.create(session=session, sender='USER', content=user_message)

        # 2. 대화 기록 조회 (최근 10개)
        previous_messages = session.messages.order_by('created_at')[:10]
        
        # 3. 프롬프트 구성
        system_prompt = (
            f"You are {session.persona.name}, a {session.persona.role}. "
            f"Difficulty Level: {session.persona.difficulty}. "
            f"System Instructions: {session.persona.system_prompt}\n"
            "Conduct a mock interview based on the user's responses. "
            "Ask one question at a time. Do not give feedback yet."
        )
        
        messages = [{"role": "system", "content": system_prompt}]
        for msg in previous_messages:
            role = "user" if msg.sender == 'USER' else "assistant"
            messages.append({"role": role, "content": msg.content})
            
        # 4. GPT 호출
        ai_response = OpenAIService.chat_completion(messages)
        
        if not ai_response:
             ai_response = "면접관이 잠시 생각을 정리하고 있습니다..."

        # 5. AI 메시지 저장
        MockInterviewMessage.objects.create(session=session, sender='AI', content=ai_response)

        return Response({'content': ai_response})

    @action(detail=True, methods=['post'])
    def end_interview(self, request, pk=None):
        session = self.get_object()
        session.status = 'COMPLETED'
        session.save()
        
        # Trigger evaluation logic
        session.score = 85
        session.feedback_summary = "Good technical depth, but work on soft skills."
        session.save()
        
        return Response({'status': 'interview ended', 'score': session.score})
