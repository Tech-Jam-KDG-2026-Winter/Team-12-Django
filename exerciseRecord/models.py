from django.db import models
from accounts.models import User


from .consts import EXERCISES

class ExerciseRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise_start_time = models.DateTimeField()
    exercise_end_time = models.DateTimeField()
    duration_minutes = models.IntegerField()

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

class ExerciseRecordDetail(models.Model):
    EXERCISE_CHOICES = []

    for category_key, category_data in EXERCISES.items():
        category_name = category_data['name']
        exercises = category_data['exercises']

        exercise_options = []
        for exercise in exercises:
            if isinstance(exercise, dict):
                name = exercise['name']
            else:
                name = exercise
            exercise_options.append((name, name))

        EXERCISE_CHOICES.append((category_name, exercise_options))

    exercise_record = models.ForeignKey(
        ExerciseRecord,
        on_delete=models.CASCADE,
        related_name='details'
    )
    exercise_type = models.CharField(max_length=100, choices=EXERCISE_CHOICES, blank=True, null=True)
    reps = models.PositiveIntegerField(blank=True, null=True, verbose_name='回数')

class FeedbackHistory(models.Model):
    """
    運動の感想履歴モデル
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
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
        return f"{self.user.username} - {self.created_at}"
