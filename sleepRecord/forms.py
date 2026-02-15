from django import forms
from .models import SleepRecord


class SleepRecordForm(forms.ModelForm):
    """
    睡眠記録の作成・編集フォーム
    """
    class Meta:
        model = SleepRecord
        fields = ['sleep_start_time', 'sleep_end_time', 'diary']
        widgets = {
            'sleep_start_time': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control'
                },
                format='%Y-%m-%dT%H:%M'
            ),
            'sleep_end_time': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control'
                },
                format='%Y-%m-%dT%H:%M'
            ),
            'diary': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': '睡眠の状態やメモを記録しましょう'
                }
            ),
        }
        labels = {
            'sleep_start_time': '就寝時刻',
            'sleep_end_time': '起床時刻',
            'diary': '日記・メモ',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # datetime-localフォーマットの設定
        self.fields['sleep_start_time'].input_formats = ['%Y-%m-%dT%H:%M']
        self.fields['sleep_end_time'].input_formats = ['%Y-%m-%dT%H:%M']

    def clean(self):
        """
        フォームバリデーション
        """
        cleaned_data = super().clean()
        sleep_start_time = cleaned_data.get('sleep_start_time')
        sleep_end_time = cleaned_data.get('sleep_end_time')

        if sleep_start_time and sleep_end_time:
            # 起床時刻が就寝時刻より前の場合はエラー
            if sleep_end_time <= sleep_start_time:
                raise forms.ValidationError(
                    '起床時刻は就寝時刻より後に設定してください。'
                )

            # 睡眠時間が24時間を超える場合は警告
            duration = SleepRecord.calculate_duration(sleep_start_time, sleep_end_time)
            if duration > 1440:  # 24時間 = 1440分
                raise forms.ValidationError(
                    '睡眠時間が24時間を超えています。正しい時刻を入力してください。'
                )

        return cleaned_data
