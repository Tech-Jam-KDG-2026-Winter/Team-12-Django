from django import forms
from .models import ExerciseRecord

class ExerciseDiaryForm(forms.ModelForm):
    """
    運動記録フォーム
    """
    class Meta:
        model = ExerciseRecord
        fields = ('diary',)
        labels = {
            'diary': '運動記録',
        }
        widgets = {
            'diary': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': '運動の内容や感想を記入してください'
            }),
        }
