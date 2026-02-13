from rest_framework import serializers
from .models import Course, Lecture, Quiz, QuizAttempt

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['id', 'question', 'options', 'correct_answer', 'explanation', 'created_at']

class LectureSerializer(serializers.ModelSerializer):
    quizzes = QuizSerializer(many=True, read_only=True)
    course_name = serializers.CharField(source='course.title', read_only=True)

    class Meta:
        model = Lecture
        fields = [
            'id', 'title', 'video_url', 'duration', 'order_index', 
            'ai_status', 'course_name', 'original_script', 
            'created_at', 'quizzes', 'script_segments', 
            'checkpoints', 'supplemental_materials'
        ]

class CourseDetailSerializer(serializers.ModelSerializer):
    lectures = LectureSerializer(many=True, read_only=True)
    instructor_name = serializers.CharField(source='instructor.nickname', read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'category', 'instructor', 'instructor_name', 'created_at', 'lectures', 'cohort_analytics']

class CourseListSerializer(serializers.ModelSerializer):
    instructor_name = serializers.CharField(source='instructor.nickname', read_only=True)
    lecture_count = serializers.IntegerField(source='lectures.count', read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'category', 'instructor_name', 'lecture_count', 'created_at', 'cohort_analytics']

class QuizAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizAttempt
        fields = ['id', 'user', 'quiz', 'is_correct', 'solved_at']
        read_only_fields = ['user', 'is_correct', 'solved_at']
