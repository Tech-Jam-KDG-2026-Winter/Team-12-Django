from django.urls import path

from . import views

urlpatterns = [
    path("",views.index_view, name="index"),
    path("post/<int:pk>/", views.post_exercise, name="post_exercise"),
    path("exercising/", views.exercising, name="exercising"),
    path("friends_exercise_records/", views.friends_execise_records, name="friends_exercise_records"),
    # path('<int:pk>/post/', views.post_exercise, name='post_exercise'),
    # path("",views.ListExerciseRecordView.as_view(), name="list-exerciseRecord"),
    # path("exerciseRecord/",views.ListExerciseRecordView.as_view(), name="list-exerciseRecord"),
    # path("exerciseRecord/<int:pk>/detail/",views.DetailBookView.as_view(), name="detail-exerciseRecord"),
    # path("exerciseRecord/create/",views.CreateBookView.as_view(), name="create-exerciseRecord"),
    # path("exerciseRecord/<int:pk>/delete/",views.DeleteBookView.as_view(), name="delete-exerciseRecord"),
    # path("exerciseRecord/<int:pk>/update/",views.UpdateBookView.as_view(), name="update-exerciseRecord"),
    # path("exerciseRecord/<int:book_id>/review/",views.CreateReviewView.as_view(), name="review"),
    # path("logout/",views.logout_view, name="logout"),
]