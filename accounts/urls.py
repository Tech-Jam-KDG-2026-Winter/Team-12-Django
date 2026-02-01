from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views as auth_views
from . import views

app_name = "accounts"

urlpatterns = [
    # path('login/', LoginView.as_view(), name="login"),
    # path('logout/', LogoutView.as_view(), name="logout"),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('signup/', views.signup, name="signup"),
]
