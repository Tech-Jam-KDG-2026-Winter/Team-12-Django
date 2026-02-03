from django.db import models
from accounts.models import User


from .consts import EXERCISES

class ExerciseRecord(models.Model):
    # EXERCISES定数からchoicesを作成
    # 形式: [('カテゴリー名', [('種目名', '種目名'), ...]), ...]
    EXERCISE_CHOICES = []
    for category_key, category_data in EXERCISES.items():
        category_name = category_data['name']
        exercises = category_data['exercises']
        exercise_options = [(exercise, exercise) for exercise in exercises]
        EXERCISE_CHOICES.append((category_name, exercise_options))

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise_start_time = models.DateTimeField()
    exercise_end_time = models.DateTimeField()
    duration_minutes = models.IntegerField()
    exercise_type = models.CharField(max_length=100, choices=EXERCISE_CHOICES, blank=True, null=True)
    diary = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.created_at}"

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