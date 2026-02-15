from django.urls import path
from . import views

app_name = 'sleepRecord'

urlpatterns = [
    # トップページ（一覧）- exerciseRecordの index と同様
    path("", views.index_view, name="index"),
    
    # 睡眠記録投稿
    path("post/<int:pk>/", views.post_sleep, name="post_sleep"),
    
    # 睡眠記録削除
    path("delete/<int:pk>/", views.remove_sleep, name="remove_sleep"),
    
    # 睡眠記録中（記録作成）
    path("sleeping/", views.sleeping, name="sleeping"),
    
    # フレンドの睡眠記録一覧
    path("friends_sleep_records/", views.friends_sleep_records, name="friends_sleep_records"),
]
