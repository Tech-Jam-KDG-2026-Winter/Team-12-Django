from django.contrib import admin
from django.utils import timezone
from .models import ExerciseRecord, ExerciseRecordDetail, FeedbackHistory

class ExerciseRecordDetailInline(admin.TabularInline):
    model = ExerciseRecordDetail
    extra = 1  # 最初から1行表示


@admin.register(ExerciseRecord)
class ExerciseRecordAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'exercise_start_time',
        'exercise_end_time',
        'duration_minutes',
        'created_at',
    )

    list_filter = ('user', 'created_at')
    search_fields = ('user__username', 'diary')
    date_hierarchy = 'created_at'

    inlines = [ExerciseRecordDetailInline]


@admin.register(ExerciseRecordDetail)
class ExerciseRecordDetailAdmin(admin.ModelAdmin):
    list_display = (
        'exercise_record',
        'exercise_type',
        'reps',
    )

    list_filter = ('exercise_type',)
    search_fields = ('exercise_type',)


@admin.register(FeedbackHistory)
class FeedbackHistoryAdmin(admin.ModelAdmin):
    list_display = ['get_user', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'feedback']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
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
