from django.test import TestCase
from django.utils import timezone
from accounts.models import User
from exerciseRecord.models import ExerciseRecord
from exerciseRecord.forms import ExerciseRecordForm

class ExerciseRecordTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.record = ExerciseRecord.objects.create(
            user=self.user,
            exercise_start_time=timezone.now(),
            exercise_end_time=timezone.now(),
            duration_minutes=30,
            diary="",
            # exercise_type is None initially
        )

    def test_exercise_type_required(self):
        # Case 1: Missing exercise_type -> Should be invalid
        form_data = {
            'exercise_type': '',
            'diary': 'Good workout'
        }
        form = ExerciseRecordForm(data=form_data, instance=self.record)
        self.assertFalse(form.is_valid())
        self.assertIn('exercise_type', form.errors)

        # Case 2: Valid exercise_type -> Should be valid
        form_data = {
            'exercise_type': 'スクワット',
            'diary': 'Good workout'
        }
        form = ExerciseRecordForm(data=form_data, instance=self.record)
        self.assertTrue(form.is_valid())
        form.save()

        self.record.refresh_from_db()
        self.assertEqual(self.record.exercise_type, 'スクワット')