from django.db import models
from accounts.models import User

class ExerciseRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise_start_time = models.DateTimeField()
    exercise_end_time = models.DateTimeField()
    duration_minutes = models.IntegerField()
    diary = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.created_at}"

    @classmethod
    def calculate_duration(cls, start_time, end_time):
        """
        開始時刻と終了時刻から運動時間（分）を計算
        """
        if start_time and end_time:
            delta = end_time - start_time
            return int(delta.total_seconds() / 60)
        return 0