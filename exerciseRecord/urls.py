from django.urls import path

from . import views

urlpatterns = [
    path("",views.index_view, name="index"),
    path("post/<int:pk>/", views.post_exercise, name="post_exercise"),
    path("exercising/", views.exercising, name="exercising"),
    path("friends_exercise_records/", views.friends_execise_records, name="friends_exercise_records"),
]