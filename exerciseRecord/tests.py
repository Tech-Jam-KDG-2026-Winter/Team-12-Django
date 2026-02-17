from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from accounts.models import User
from .models import ExerciseRecord
from .forms import ExerciseRecordForm


class ExerciseRecordTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.now = timezone.now()
        self.record = ExerciseRecord.objects.create(
            user=self.user,
            exercise_start_time=self.now - timedelta(minutes=30),
            exercise_end_time=self.now,
            duration_minutes=30,
            exercise_types=['スクワット', 'ベンチプレス'],
            diary='テスト日記'
        )

    def test_exercise_types_display(self):
        """exercise_types_displayプロパティが正しく動作する"""
        self.assertEqual(
            self.record.exercise_types_display,
            "スクワット, ベンチプレス"
        )

    def test_exercise_types_display_empty(self):
        """exercise_typesが空の場合、'その他'を返す"""
        self.record.exercise_types = []
        self.assertEqual(self.record.exercise_types_display, "その他")

    def test_exercise_types_optional(self):
        """exercise_typesは任意フィールドなので空でもバリデーション通過する"""
        form = ExerciseRecordForm(data={
            'exercise_types': [],
            'diary': 'テスト',
            'reps': '',
        })
        self.assertTrue(form.is_valid())

    def test_exercise_types_with_selection(self):
        """exercise_typesに種目を選択した場合、正しく保存される"""
        form = ExerciseRecordForm(data={
            'exercise_types': ['スクワット'],
            'diary': 'テスト',
            'reps': '',
        }, instance=self.record)
        self.assertTrue(form.is_valid())
        saved = form.save()
        self.assertEqual(saved.exercise_types, ['スクワット'])

    def test_exercise_types_multiple_selection(self):
        """exercise_typesに複数種目を選択した場合、正しく保存される"""
        form = ExerciseRecordForm(data={
            'exercise_types': ['スクワット', 'ベンチプレス', 'デッドリフト'],
            'diary': 'テスト',
            'reps': '',
        }, instance=self.record)
        self.assertTrue(form.is_valid())
        saved = form.save()
        self.assertEqual(saved.exercise_types, ['スクワット', 'ベンチプレス', 'デッドリフト'])

    def test_reps_optional(self):
        """repsは任意フィールドなので空でもバリデーション通過する"""
        form = ExerciseRecordForm(data={
            'exercise_types': ['スクワット'],
            'diary': 'テスト',
            'reps': '',
        }, instance=self.record)
        self.assertTrue(form.is_valid())

    def test_reps_with_value(self):
        """repsに値を設定した場合、正しく保存される"""
        form = ExerciseRecordForm(data={
            'exercise_types': ['スクワット'],
            'diary': 'テスト',
            'reps': '15',
        }, instance=self.record)
        self.assertTrue(form.is_valid())
        saved = form.save()
        self.assertEqual(saved.reps, 15)

    def test_duration_display(self):
        """duration_displayプロパティが正しく動作する"""
        start = self.now - timedelta(minutes=45)
        end = self.now
        record = ExerciseRecord.objects.create(
            user=self.user,
            exercise_start_time=start,
            exercise_end_time=end,
            duration_minutes=45,
            diary='テスト'
        )
        self.assertEqual(record.duration_display, "45分")