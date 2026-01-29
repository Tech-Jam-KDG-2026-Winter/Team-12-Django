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
    created_at = models.DateTimeField(auto_now_add=True)

    def sleep_duration(self):
        return self.exercise_end_time - self.exercise_start_time

    def __str__(self):
        return f"{self.user.username} - {self.created_at}"

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