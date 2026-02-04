from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    カスタムユーザー管理画面
    """
    # 一覧画面で表示するフィールド
    list_display = ('username', 'email', 'username', 'is_staff', 'last_exercise_time')

    # 詳細画面のフィールドセット
    fieldsets = UserAdmin.fieldsets + (
        ('追加情報', {
            'fields': ('last_exercise_time', 'profile_image')
        }),
    )

    # 新規作成画面のフィールドセット
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('追加情報', {
            'fields': ('last_exercise_time', 'profile_image')
        }),
    )