from django.urls import path

from . import views

urlpatterns = [
    path("", views.index_view, name="index"),
    path("post/<int:pk>/", views.post_exercise, name="post_exercise"),
    path("delete/<int:pk>/", views.remove_exercise, name="remove_exercise"),
    path("exercising/", views.exercising, name="exercising"),
    path("friends_exercise_records/", views.friends_execise_records, name="friends_exercise_records"),
    path("feedback/<int:pk>/save/", views.save_feedback, name="save_feedback"),
    path("feedback/<int:pk>/", views.feedback_history, name="feedback_history"),
    path("feedbacks/", views.feedback_list, name="feedback_list"),
]
