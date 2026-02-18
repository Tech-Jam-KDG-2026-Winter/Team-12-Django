from django.contrib import admin
from django.utils import timezone
from .models import ExerciseRecord, FeedbackHistory


@admin.register(ExerciseRecord)
class ExerciseRecordAdmin(admin.ModelAdmin):
    list_display = ['user', 'exercise_types_display', 'reps', 'exercise_start_time', 'exercise_end_time', 'duration_display', 'created_at']
    list_filter = ['created_at', 'user']
    search_fields = ['user__username', 'diary']
    ordering = ['-created_at']

    fieldsets = (
        ('ユーザー情報', {
            'fields': ('user',)
        }),
        ('運動情報', {
            'fields': ('exercise_types', 'refs' 'exercise_start_time', 'exercise_end_time')
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

    def exercise_types_display(self, obj):
        """一覧画面で運動種目を表示"""
        return obj.exercise_types_display
    exercise_types_display.short_description = '運動種目'


@admin.register(FeedbackHistory)
class FeedbackHistoryAdmin(admin.ModelAdmin):
    list_display = ['get_user', 'get_exercise_types', 'get_exercise_date', 'created_at']
    list_filter = ['created_at', 'exercise_record__exercise_type']
    search_fields = ['exercise_record__user__username', 'feedback']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('運動情報', {
            'fields': ('exercise_record',)
        }),
        ('感想', {
            'fields': ('feedback',)
        }),
        ('日時情報', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_user(self, obj):
        """ユーザー名を表示"""
        return obj.exercise_record.user.username
    get_user.short_description = 'ユーザー'

    def get_exercise_date(self, obj):
        """運動日時を表示"""
        return obj.exercise_record.exercise_end_time
    get_exercise_date.short_description = '運動日時'
