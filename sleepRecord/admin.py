from django.contrib import admin
from .models import SleepRecord


@admin.register(SleepRecord)
class SleepRecordAdmin(admin.ModelAdmin):
    """
    睡眠記録の管理画面設定
    """
    list_display = [
        'user',
        'sleep_start_time',
        'sleep_end_time',
        'duration_display',
        'created_at'
    ]
    list_filter = ['created_at', 'user']
    search_fields = ['user__username', 'diary']
    date_hierarchy = 'sleep_start_time'
    
    readonly_fields = ['created_at', 'duration_display']
    
    fieldsets = (
        ('基本情報', {
            'fields': ('user', 'sleep_start_time', 'sleep_end_time', 'duration_minutes')
        }),
        ('詳細', {
            'fields': ('diary',)
        }),
        ('システム情報', {
            'fields': ('created_at', 'duration_display'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """
        クエリセットの最適化
        """
        qs = super().get_queryset(request)
        return qs.select_related('user')
