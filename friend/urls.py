from django.urls import include, path
from . import views

app_name = "friend"

urlpatterns = [
    # path('', include("exerciseRecord.urls")),
    path("search/", views.user_search, name="user_search"),
    path("friends/", views.friends_list, name="friends_list"),
    path('requests/', views.friend_requests, name='friend_requests'),
    path('sent_requests/', views.sent_requests, name='sent_requests'),
    path('requests/accept/<int:request_id>/', views.accept_friend_request, name='accept_request'),
    path('requests/reject/<int:request_id>/', views.reject_friend_request, name='reject_request'),
    path("send_friend_request/<int:user_id>/",views.send_friend_request,name="send_friend_request"),
    path("cancel_friend_request/<int:request_id>/",views.cancel_friend_request,name="cancel_friend_request"),
    path("remove_friend/<int:friend_id>/",views.remove_friend,name="remove_friend"),
]