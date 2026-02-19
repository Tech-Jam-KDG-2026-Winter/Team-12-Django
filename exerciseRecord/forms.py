from django import forms
from django.forms import inlineformset_factory
from .models import ExerciseRecord, ExerciseRecordDetail, FeedbackHistory

# Detail用フォーム
class ExerciseRecordDetailForm(forms.ModelForm):
    class Meta:
        model = ExerciseRecordDetail
        fields = ('exercise_type', 'reps')
        widgets = {
            'exercise_type': forms.Select(attrs={'class': 'form-control'}),
            'reps': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '回数を入力',
                'min': 1
            }),
        }

# ExerciseRecord用フォーム
class ExerciseRecordForm(forms.ModelForm):
    class Meta:
        model = ExerciseRecord
        fields = ('diary',)
        widgets = {
            'diary': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': '運動の内容や感想を記入してください'
            }),
        }

# Formset を作成
ExerciseRecordDetailFormSet = inlineformset_factory(
    ExerciseRecord,
    ExerciseRecordDetail,
    form=ExerciseRecordDetailForm,
    extra=1,
    can_delete=True
)

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
