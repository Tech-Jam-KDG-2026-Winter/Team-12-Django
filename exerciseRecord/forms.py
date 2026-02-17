from django import forms
from .models import ExerciseRecord, FeedbackHistory

class ExerciseRecordForm(forms.ModelForm):
    exercise_type = forms.ChoiceField(choices=ExerciseRecord.EXERCISE_CHOICES, required=True, label='種目', widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = ExerciseRecord
        fields = ('exercise_type', 'diary',)
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


class FeedbackHistoryForm(forms.ModelForm):
    """感想履歴フォーム"""
    class Meta:
        model = FeedbackHistory
        fields = ('feedback',)
        labels = {
            'feedback': '感想',
        }
        widgets = {
            'feedback': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': '運動についての感想を記入してください'
            }),
        }
