from django.db import models
from accounts.models import User


from .consts import EXERCISES


class ExerciseRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise_start_time = models.DateTimeField()
    exercise_end_time = models.DateTimeField()
    duration_minutes = models.IntegerField()

    # 複数選択できるように、リストで保存
    exercise_types = models.JSONField(
        default=list,
        blank=True
    )
    # 回数記録（任意）
    reps = models.PositiveIntegerField(blank=True, null=True, verbose_name='回数')
    diary = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'exercise_records'
        verbose_name = '運動記録'
        verbose_name_plural = '運動記録'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.created_at}"

    # consts.pyから選択肢を取得
    @classmethod
    def get_exercise_choices(cls):
        """フォームで使う選択肢を生成"""
        choices = []
        for category_key, category_data in EXERCISES.items():
            for exercise in category_data['exercises']:
                name = exercise['name'] if isinstance(exercise, dict) else exercise
                choices.append((name, name))
        return choices

    @classmethod
    def get_exercise_choices_by_category(cls):
        """カテゴリー別の運動種目選択肢を取得"""
        choices_by_category = {}
        for category_key, category_data in EXERCISES.items():
            category_name = category_data['name']
            choices_by_category[category_name] = category_data['exercises']
        return choices_by_category

    @property
    def exercise_types_display(self):
        """選択された運動種目を文字列で返す"""
        if isinstance(self.exercise_types, list) and self.exercise_types:
            return ", ".join(self.exercise_types)
        return "その他"
    
    @property
    def duration_display(self):
        if self.exercise_start_time and self.exercise_end_time:
            delta = self.exercise_end_time - self.exercise_start_time
            total_seconds = int(delta.total_seconds())
            if total_seconds < 60:
                return f"{total_seconds}秒"

        hours = self.duration_minutes // 60
        minutes = self.duration_minutes % 60
        if hours > 0:
            return f"{hours}時間{minutes}分"
        return f"{minutes}分"

    @classmethod
    def calculate_duration(cls, start_time, end_time):
        """
        開始時刻と終了時刻から運動時間（分）を計算
        """
        if start_time and end_time:
            delta = end_time - start_time
            return int(delta.total_seconds() / 60)
        return 0

class FeedbackHistory(models.Model):
    """
    運動の感想履歴モデル
    """
    exercise_record = models.OneToOneField(
        ExerciseRecord,
        on_delete=models.CASCADE,
        related_name='feedback_history'
    )
    feedback = models.TextField(
        help_text="運動についての感想"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = '感想履歴'
        verbose_name_plural = '感想履歴'

    def __str__(self):
        return f"{self.exercise_record.user.username} - {self.created_at}"
