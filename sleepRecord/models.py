from django.db import models
from accounts.models import User

class SleepRecord(models.Model):
    """
    睡眠記録モデル
    ExerciseRecordと同様の構造で睡眠記録を管理
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sleep_start_time = models.DateTimeField(verbose_name='就寝時刻')
    sleep_end_time = models.DateTimeField(verbose_name='起床時刻')
    duration_minutes = models.IntegerField(verbose_name='睡眠時間（分）')
    diary = models.TextField(blank=True, verbose_name='日記・メモ')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-sleep_start_time']
        verbose_name = '睡眠記録'
        verbose_name_plural = '睡眠記録'

    def __str__(self):
        return f"{self.user.username} - {self.sleep_start_time.strftime('%Y-%m-%d')}"

    @property
    def duration_display(self):
        """
        睡眠時間を読みやすい形式で表示
        """
        if self.sleep_start_time and self.sleep_end_time:
            delta = self.sleep_end_time - self.sleep_start_time
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
        就寝時刻と起床時刻から睡眠時間（分）を計算
        """
        if start_time and end_time:
            delta = end_time - start_time
            return int(delta.total_seconds() / 60)
        return 0

    def save(self, *args, **kwargs):
        """
        保存時に自動的に睡眠時間を計算
        """
        if self.sleep_start_time and self.sleep_end_time and not self.duration_minutes:
            self.duration_minutes = self.calculate_duration(
                self.sleep_start_time,
                self.sleep_end_time
            )
        super().save(*args, **kwargs)
