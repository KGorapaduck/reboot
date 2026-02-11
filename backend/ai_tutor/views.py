from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import LectureNote, AIChatSession, AIChatMessage
from .serializers import LectureNoteSerializer, AIChatSessionSerializer, AIChatMessageSerializer

class LectureNoteViewSet(viewsets.ModelViewSet):
    # queryset will be filtered by user
    serializer_class = LectureNoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return LectureNote.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def create_custom(self, request):
        # Logic to create a custom note or request AI regeneration
        pass
from .rag_service import RAGService

class AIChatSessionViewSet(viewsets.ModelViewSet):
    serializer_class = AIChatSessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return AIChatSession.objects.filter(user=self.request.user)

    @action(detail=True, methods=['post'])
    def chat(self, request, pk=None):
        session = self.get_object()
        user_message = request.data.get('message')
        
        # Save user message
        AIChatMessage.objects.create(session=session, sender='USER', message=user_message)

        # 1. RAG: 관련 강의 검색
        # 현재 세션의 강의 컨텍스트를 우선적으로 고려할 수도 있음
        similar_lectures = RAGService.find_similar_lectures(user_message, limit=3)
        
        # 2. GPT: 답변 생성
        if similar_lectures:
            ai_response = RAGService.generate_answer(user_message, similar_lectures)
        else:
            ai_response = "죄송합니다. 질문과 관련된 강의 내용을 찾을 수 없습니다."
        
        if not ai_response:
             ai_response = "AI 서비스 연결에 문제가 발생했습니다. (API Key 확인 필요)"

        # Save AI message
        AIChatMessage.objects.create(session=session, sender='AI', message=ai_response)
        
        return Response({'response': ai_response})
