from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    """
    カスタムユーザー
    """
    last_exercise_time = models.DateTimeField(
        null=True,
        blank=True,
        help_text="最後に運動を始めた時間"
    )

    def __str__(self):
        return self.username

class ExerciseRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise_start_time = models.DateTimeField()
    exercise_end_time = models.DateTimeField()
    diary = models.TextField(blank=True)
    # 運動時間（分単位で保存）
    duration_minutes = models.IntegerField()
    # 記録日時（自動設定）
    created_at = models.DateTimeField(auto_now_add=True,)

    class Meta:
        ordering = ['-created_at']
        verbose_name = '運動記録'
        verbose_name_plural = '運動記録'
    
    def __str__(self):
        return f"{self.user.username} - {self.created_at.strftime('%Y/%m/%d %H:%M')}"
    
    @property
    def duration_display(self):
        """
        運動時間を「〇時間〇分」形式で表示するプロパティ
        """
        if self.duration_minutes is not None:
            if self.duration_minutes == 0:
                return "1分未満"
            
            hours = self.duration_minutes // 60
            minutes = self.duration_minutes % 60
            
            if hours > 0:
                if minutes > 0:
                    return f"{hours}時間{minutes}分"
                else:
                    return f"{hours}時間"
            else:
                return f"{minutes}分"
        
        return "不明"
    
    @classmethod
    def calculate_duration(cls, start_time, end_time):
        """
        開始時刻と終了時刻から運動時間（分）を計算
        """
        if start_time and end_time:
            delta = end_time - start_time
            return int(delta.total_seconds() / 60)
        return 0

class FriendRequest(models.Model):
    from_user = models.ForeignKey(
        User,
        related_name='sent_requests',
        on_delete=models.CASCADE
    )
    to_user = models.ForeignKey(
        User,
        related_name='received_requests',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.from_user} - {self.to_user}"

class FriendRequest(models.Model):
    from_user = models.ForeignKey(
        User,
        related_name='sent_requests',
        on_delete=models.CASCADE
    )
    to_user = models.ForeignKey(
        User,
        related_name='received_requests',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.from_user} → {self.to_user}"

class Friend(models.Model):
    user1 = models.ForeignKey(
        User,
        related_name='friends1',
        on_delete=models.CASCADE
    )
    user2 = models.ForeignKey(
        User,
        related_name='friends2',
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('user1', 'user2')

    def __str__(self):
        return f"{self.user1} & {self.user2}"