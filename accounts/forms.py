from django.contrib.auth.forms import UserCreationForm
from .models import User



class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",'profile_image')

    # profile_imageを必須ではなくする
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profile_image'].required = False