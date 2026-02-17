from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", 'profile_image')

    # profile_imageを必須ではなくする
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profile_image'].required = False


class ProfileEditForm(forms.ModelForm):
    """プロフィール編集フォーム"""
    class Meta:
        model = User
        fields = ('profile_image', 'twitter_url', 'instagram_url')
        labels = {
            'profile_image': 'プロフィール画像',
            'twitter_url': 'X (Twitter) URL',
            'instagram_url': 'Instagram URL',
        }
        widgets = {
            'profile_image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'twitter_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://x.com/username'
            }),
            'instagram_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://instagram.com/username'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # すべてのフィールドを必須ではなくする
        self.fields['profile_image'].required = False
        self.fields['twitter_url'].required = False
        self.fields['instagram_url'].required = False
