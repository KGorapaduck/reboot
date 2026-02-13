from django.contrib import admin
from .models import Curriculum, CurriculumItem, ReroutingLog

@admin.register(Curriculum)
class CurriculumAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'status', 'start_date', 'target_date')
    list_filter = ('status',)

@admin.register(CurriculumItem)
class CurriculumItemAdmin(admin.ModelAdmin):
    list_display = ('curriculum', 'lecture', 'is_completed', 'order_index')
    list_filter = ('is_completed',)

@admin.register(ReroutingLog)
class ReroutingLogAdmin(admin.ModelAdmin):
    list_display = ('curriculum', 'reason', 'created_at')
