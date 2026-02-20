from django.contrib import admin
from django.utils import timezone
from django import forms
from .models import ExerciseRecord, FeedbackHistory
import json


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
            'fields': ('exercise_types', 'reps', 'exercise_start_time', 'exercise_end_time')
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
    list_display = ['get_user', 'get_exercise_types_display', 'get_exercise_date', 'created_at']
    list_filter = ['created_at']
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

    def get_exercise_types_display(self, obj):
        """運動種目を表示（複数対応）"""
        return obj.exercise_record.exercise_types_display
    get_exercise_types_display.short_description = '運動種目'

    def get_exercise_date(self, obj):
        """運動日時を表示"""
        return obj.exercise_record.exercise_end_time
    get_exercise_date.short_description = '運動日時'


class ExerciseRecordAdminForm(forms.ModelForm):
    """運動記録の管理画面用フォーム"""
    
    # exercise_typesを編集しやすいテキストエリアに
    exercise_types_input = forms.CharField(
        label='運動種目と回数',
        widget=forms.Textarea(attrs={'rows': 5, 'cols': 60}),
        required=False,
        help_text='例: [{"type": "スクワット", "reps": 20}, {"type": "腕立て伏せ", "reps": 15}]'
    )
    
    class Meta:
        model = ExerciseRecord
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.exercise_types:
            # 既存データを整形して表示
            self.initial['exercise_types_input'] = json.dumps(
                self.instance.exercise_types, 
                ensure_ascii=False, 
                indent=2
            )
    
    def clean_exercise_types_input(self):
        """入力されたJSONをパース"""
        data = self.cleaned_data.get('exercise_types_input', '')
        if not data:
            return []
        
        try:
            parsed = json.loads(data)
            if not isinstance(parsed, list):
                raise forms.ValidationError('リスト形式で入力してください')
            return parsed
        except json.JSONDecodeError:
            raise forms.ValidationError('正しいJSON形式で入力してください')
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.exercise_types = self.cleaned_data.get('exercise_types_input', [])
        if commit:
            instance.save()
        return instance