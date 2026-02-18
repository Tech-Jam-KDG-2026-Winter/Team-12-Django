from django.shortcuts import render, redirect
from .forms import SignUpForm, ProfileEditForm
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.http import JsonResponse
import json
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

# Create your views here.

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            user = form.save()
            auth_login(request, user)
            messages.success(request, 'アカウントを作成しました。')
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, "accounts/signup.html", {"form": form})


@login_required
def profile_edit(request):
    """プロフィール編集ページを表示・処理するビュー"""
    if request.method == "POST":
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'プロフィールを更新しました。')
            return redirect('index')
    else:
        form = ProfileEditForm(instance=request.user)
    
    return render(request, "accounts/profile_edit.html", {"form": form})


@login_required
@require_POST
def update_profile(request):
    try:
        new_username = None
        profile_image = None
        twitter_url = None
        instagram_url = None
        has_username_field = False
        
        # Handle JSON request
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            if 'username' in data:
                new_username = data.get('username')
                has_username_field = True
            if 'twitter_url' in data:
                twitter_url = data.get('twitter_url')
            if 'instagram_url' in data:
                instagram_url = data.get('instagram_url')
        # Handle Form/Multipart request
        else:
            if 'username' in request.POST:
                new_username = request.POST.get('username')
                has_username_field = True
            profile_image = request.FILES.get('profile_image')
            if 'twitter_url' in request.POST:
                twitter_url = request.POST.get('twitter_url')
            if 'instagram_url' in request.POST:
                instagram_url = request.POST.get('instagram_url')
        
        response_data = {'status': 'success', 'message': 'Profile updated successfully'}
        # Validation for empty username if field was present
        if has_username_field and not new_username:
             return JsonResponse({'status': 'error', 'message': 'Username is required'}, status=400)
        changes_made = False

        # Update Username
        if new_username:
             if request.user.username != new_username:
                # Check if username is already taken
                from django.contrib.auth import get_user_model
                User = get_user_model()
                if User.objects.filter(username=new_username).exclude(pk=request.user.pk).exists():
                    return JsonResponse({'status': 'error', 'message': 'このユーザー名は既に使用されています。'}, status=400)
                request.user.username = new_username
                changes_made = True
                response_data['message'] = 'Username updated'

        # Update Profile Image
        if profile_image:
            request.user.profile_image = profile_image
            changes_made = True
            response_data['message'] = 'Profile image updated'
        
        # Update Twitter URL
        if twitter_url is not None:
            request.user.twitter_url = twitter_url
            changes_made = True
        
        # Update Instagram URL
        if instagram_url is not None:
            request.user.instagram_url = instagram_url
            changes_made = True
        
        if changes_made:
             request.user.save()
             if new_username and profile_image:
                 response_data['message'] = 'Profile updated'
        else:
             if has_username_field and request.user.username == new_username and not profile_image:
                return JsonResponse({'status': 'success', 'message': 'Username unchanged'})
        # Return new image URL if existed
        if request.user.profile_image:
            response_data['image_url'] = request.user.profile_image.url
        
        return JsonResponse(response_data)
        
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
