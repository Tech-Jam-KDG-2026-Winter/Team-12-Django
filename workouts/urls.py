from django.urls import include, path

urlpatterns = [
    path('', include("exerciseRecord.urls")),
    path('accounts/', include("accounts.urls")),
    path('friend/', include("friend.urls")),
]