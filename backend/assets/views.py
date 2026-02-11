from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import SkillBlock, UserSkill, Portfolio, PortfolioProject
from .serializers import SkillBlockSerializer, UserSkillSerializer, PortfolioSerializer

class SkillBlockViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SkillBlock.objects.all()
    serializer_class = SkillBlockSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserSkillViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSkillSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserSkill.objects.filter(user=self.request.user)

from core.services import OpenAIService

class PortfolioViewSet(viewsets.ModelViewSet):
    serializer_class = PortfolioSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Portfolio.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def generate(self, request, pk=None):
        portfolio = self.get_object()
        
        # 1. 관련 스킬 및 프로젝트 데이터 수집
        projects = portfolio.projects.all()
        project_texts = [f"- {p.name}: {p.description}" for p in projects]
        projects_summary = "\n".join(project_texts)
        
        user_skills = UserSkill.objects.filter(user=request.user)
        skill_texts = [f"- {s.skill_block.name} ({s.skill_block.category})" for s in user_skills]
        skills_summary = "\n".join(skill_texts)
        
        # 2. 프롬프트 구성
        doc_type = "RESUME" if portfolio.type == 'RESUME' else "BUSINESS PLAN"
        
        system_prompt = (
            f"You are a professional career consultant. "
            f"Write a professional {doc_type} in Markdown format based on the user's skills and projects."
        )
        
        user_prompt = (
            f"Title: {portfolio.title}\n"
            f"User Data:\n{portfolio.sections}\n\n"
            f"Acquired Skills:\n{skills_summary}\n\n"
            f"Key Projects:\n{projects_summary}\n\n"
            "Please compile this into a structured, high-quality document."
        )
        
        # 3. GPT 호출
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        generated_content = OpenAIService.chat_completion(messages)
        
        if generated_content:
            portfolio.compiled_markdown = generated_content
            portfolio.save()
            return Response({'markdown': portfolio.compiled_markdown})
        else:
            return Response({'error': 'Failed to generate content'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
