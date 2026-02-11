from rest_framework import serializers
from .models import SkillBlock, UserSkill, Portfolio, PortfolioProject

class SkillBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillBlock
        fields = ['id', 'course', 'name', 'category', 'criteria']

class UserSkillSerializer(serializers.ModelSerializer):
    skill_block = SkillBlockSerializer(read_only=True)

    class Meta:
        model = UserSkill
        fields = ['id', 'user', 'skill_block', 'acquired_at', 'verification_source']
        read_only_fields = ['user', 'acquired_at']

class PortfolioProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioProject
        fields = ['id', 'portfolio', 'skill_block', 'name', 'description']

class PortfolioSerializer(serializers.ModelSerializer):
    projects = PortfolioProjectSerializer(many=True)

    class Meta:
        model = Portfolio
        fields = ['id', 'user', 'title', 'type', 'sections', 'compiled_markdown', 'created_at', 'projects']
        read_only_fields = ['user', 'created_at', 'compiled_markdown']

    def create(self, validated_data):
        projects_data = validated_data.pop('projects', [])
        portfolio = Portfolio.objects.create(**validated_data)
        for project_data in projects_data:
            PortfolioProject.objects.create(portfolio=portfolio, **project_data)
        return portfolio
