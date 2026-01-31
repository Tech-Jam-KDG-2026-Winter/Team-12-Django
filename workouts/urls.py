from django.urls import path
from . import views

app_name = 'workouts'

urlpatterns = [
    # トップページ
    path('', views.index, name='index'),
    
    # タイマーページ
    path('timer/', views.timer, name='timer'),
    
    # 投稿画面
    path('<int:pk>/post/', views.post_exercise, name='post_exercise'),
]
