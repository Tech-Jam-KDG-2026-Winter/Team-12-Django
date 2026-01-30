from django import forms
from .models import ExerciseRecord

class ExerciseRecordForm(forms.ModelForm):
    class Meta:
        model = ExerciseRecord
        fields = ['diary']
        widgets = {'diary': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),}