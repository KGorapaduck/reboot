from rest_framework import serializers
from .models import Curriculum, CurriculumItem, ReroutingLog
from lectures.serializers import LectureSerializer

class CurriculumItemSerializer(serializers.ModelSerializer):
    lecture = LectureSerializer(read_only=True)

    class Meta:
        model = CurriculumItem
        fields = ['id', 'lecture', 'order_index', 'is_completed', 'completed_at']
        read_only_fields = ['lecture', 'completed_at']

class ReroutingLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReroutingLog
        fields = ['id', 'reason', 'old_path', 'new_path', 'created_at']

class CurriculumDetailSerializer(serializers.ModelSerializer):
    items = CurriculumItemSerializer(many=True, read_only=True)
    rerouting_logs = ReroutingLogSerializer(many=True, read_only=True)

    class Meta:
        model = Curriculum
        fields = ['id', 'user', 'course', 'status', 'start_date', 'target_date', 'items', 'rerouting_logs']
        read_only_fields = ['user', 'course', 'start_date', 'items', 'rerouting_logs']
