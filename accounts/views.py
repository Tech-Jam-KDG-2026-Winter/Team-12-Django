from django.shortcuts import render, redirect
from .forms import SignUpForm as UserCreationForm
from django.contrib import messages
from django.contrib.auth import login as auth_login

# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, 'アカウントを作成しました。')
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})