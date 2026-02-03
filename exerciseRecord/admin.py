from django.contrib import admin
from django.utils import timezone
from .models import ExerciseRecord


@admin.register(ExerciseRecord)
class ExerciseRecordAdmin(admin.ModelAdmin):
    list_display = ['user', 'exercise_type', 'exercise_start_time', 'exercise_end_time', 'duration_display', 'created_at']
    list_filter = ['exercise_type', 'created_at']
    search_fields = ['user__username', 'exercise_type', 'diary']
    ordering = ['-created_at']

    fieldsets = (
        ('ユーザー情報', {
            'fields': ('user',)
        }),
        ('運動情報', {
            'fields': ('exercise_type', 'exercise_start_time', 'exercise_end_time')
        }),
        ('感想', {
            'fields': ('diary',),
            'classes': ('collapse',)
        }),
    )

    exclude = ['duration_minutes']

    def save_model(self, request, obj, form, change):
        """
        保存時にduration_minutesを自動計算
        """
        obj.duration_minutes = ExerciseRecord.calculate_duration(
            obj.exercise_start_time,
            obj.exercise_end_time
        )
        super().save_model(request, obj, form, change)

    def duration_display(self, obj):
        """
        一覧画面で運動時間を表示
        """
        return obj.duration_display

    duration_display.short_description = '運動時間'