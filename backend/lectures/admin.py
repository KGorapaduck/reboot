from django.contrib import admin
from .models import Course, Lecture, Quiz, QuizAttempt

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'instructor', 'created_at')
    search_fields = ('title', 'description')

@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order_index', 'ai_status')
    list_filter = ('ai_status', 'course')
    search_fields = ('title', 'original_script')
    # JSON fields are automatically handled by Django admin, but we can make them prettier if needed.
    # For now, default widget is fine.

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('lecture', 'created_at')

@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'is_correct', 'solved_at')
    list_filter = ('is_correct',)
