from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
import json
import os

User = get_user_model()

class UpdateProfileViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.other_user = User.objects.create_user(username='otheruser', password='password')
        self.url = reverse('accounts:update_profile')

    def tearDown(self):
        # Clean up uploaded files
        if self.user.profile_image and self.user.profile_image.name != 'profile_images/default_profile.png':
            if os.path.isfile(self.user.profile_image.path):
                os.remove(self.user.profile_image.path)

    def test_update_profile_success_json(self):
        self.client.login(username='testuser', password='password')
        data = {'username': 'newusername'}
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'newusername')

    def test_update_profile_success_multipart(self):
        self.client.login(username='testuser', password='password')
        data = {'username': 'newusername_form'}
        response = self.client.post(self.url, data) # Default is multipart/form-data when data is dict
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'newusername_form')

    def test_update_profile_image_upload(self):
        self.client.login(username='testuser', password='password')
        image_content = b'fakeimagecontent'
        image = SimpleUploadedFile("test_image.jpg", image_content, content_type="image/jpeg")
        
        data = {'profile_image': image}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')
        
        self.user.refresh_from_db()
        self.assertTrue(self.user.profile_image.name.startswith('profile_images/test_image'))
        self.assertIn('image_url', response.json())

    def test_update_profile_unauthenticated(self):
        data = {'username': 'newusername'}
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        # Should redirect to login page (302)
        self.assertEqual(response.status_code, 302)

    def test_update_profile_existing_username(self):
        self.client.login(username='testuser', password='password')
        data = {'username': 'otheruser'}
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['status'], 'error')
        self.assertEqual(response.json()['message'], 'Username already taken')

    def test_update_profile_empty_username(self):
        self.client.login(username='testuser', password='password')
        data = {'username': ''}
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['status'], 'error')

    def test_update_profile_same_username(self):
        self.client.login(username='testuser', password='password')
        data = {'username': 'testuser'}
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')
        self.assertEqual(response.json()['message'], 'Username unchanged')
