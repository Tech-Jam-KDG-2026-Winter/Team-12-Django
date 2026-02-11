from django import forms
from .models import ExerciseRecord

class ExerciseRecordForm(forms.ModelForm):
    exercise_type = forms.ChoiceField(choices=ExerciseRecord.EXERCISE_CHOICES, required=True, label='種目', widget=forms.Select(attrs={'class': 'form-control'}))
    reps = forms.IntegerField(required=False, label='回数', min_value=1, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '回数を入力'}))

    class Meta:
        model = ExerciseRecord
        fields = ('exercise_type', 'reps', 'diary',)
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