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