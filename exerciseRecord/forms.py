from django import forms
from .models import ExerciseRecord

class ExerciseRecordForm(forms.ModelForm):
    # 複数選択できるフィールド
    exercise_types = forms.MultipleChoiceField(
        label='運動種目',
        choices=[],
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # consts.pyから選択肢を取得
        self.fields['exercise_types'].choices = ExerciseRecord.get_exercise_choices()
        
        # 既存のレコードを編集する場合、選択済みの値を設定
        if self.instance and self.instance.pk:
            if isinstance(self.instance.exercise_types, list):
                self.initial['exercise_types'] = self.instance.exercise_types
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        # 選択された運動種目をリストとして保存
        instance.exercise_types = self.cleaned_data.get('exercise_types', [])
        if commit:
            instance.save()
        return instance