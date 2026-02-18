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
    profile_image = models.ImageField(
        upload_to='profile_images/',  # MEDIA_ROOT/profile_images/ に保存
        blank=True,
        null=True,
        default='profile_images/default_profile.png'  # デフォルト画像
    )
    twitter_url = models.URLField(
        max_length=200,
        blank=True,
        null=True,
        help_text="X (Twitter) プロフィールの URL"
    )
    instagram_url = models.URLField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Instagram プロフィールの URL"
    )

    last_sleep_time = models.DateTimeField(
        null=True, 
        blank=True, 
        verbose_name="最終睡眠開始時刻"
    )

    def __str__(self):
        return self.username
