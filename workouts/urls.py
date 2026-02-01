from django.urls import include, path
from . import views

urlpatterns = [
    path('', include("exerciseRecord.urls")),
    path('accounts/', include("accounts.urls")),
    path('friend/', include("friend.urls")),
]