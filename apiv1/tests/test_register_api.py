from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class RegisterAPITestCase(APITestCase):
    """Test for registration api"""

    def setUp(self):
        User.objects.create_user(username='admin', password='test12345', email='test@test.com')

        self.url = reverse('register')

    def test_user_registration(self):
        data = {'username': 'test',
                'email': 'test@example.com',
                'first_name': 'Test',
                'last_name': 'Test',
                'password': 'test12345',
                'password2': 'test12345'}
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

    def test_email_validation(self):
        data = {'username': 'test',
                'email': 'test@test.com',
                'first_name': 'Test',
                'last_name': 'Test',
                'password': 'test12345',
                'password2': 'test12345'}
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_validation(self):
        data = {'username': 'test',
                'email': 'someemail@test.com',
                'first_name': 'Test',
                'last_name': 'Test',
                'password': 'test12345',
                'password2': 'testtest'}
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
