from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class UserAPITestCase(APITestCase):
    """Test for user api"""

    def setUp(self):
        self.superuser = User.objects.create_superuser(
            username='admin', password='test12345', email='admin@admin.com')
        self.regular_user = User.objects.create_user(
            username='test', password='test54321', email='test@test.com')

        self.data = {
            'username': 'John',
            'email': 'john@test.com',
            'password': '1111'
        }

    def test_user_list_if_admin(self):
        """Check if admin can get a user list"""

        url = reverse('user-list')
        self.client.login(username='admin', password='test12345')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['results']), 2)

    def test_user_list_if_regular_user(self):
        """Check if GET user list returns 403 status if user is not admin"""

        url = reverse('user-list')
        self.client.login(username='test', password='test54321')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_list_if_anonymous(self):
        """Check if GET user list returns 403 status if user is anonymous"""

        url = reverse('user-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_user_if_admin(self):
        """Check if admin can get a user detail"""

        url = reverse('user-detail', args=[self.regular_user.pk])
        self.client.login(username='admin', password='test12345')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['username'], 'test')
        self.assertEqual(response.json()['email'], 'test@test.com')

    def test_get_user_if_regular_user(self):
        """Check if GET user returns 403 status if user is not admin"""

        url = reverse('user-detail', args=[self.regular_user.pk])
        self.client.login(username='test', password='test54321')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_user_if_anonymous(self):
        """Check if GET user returns 403 status if user is anonymous"""

        url = reverse('user-detail', args=[self.regular_user.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_user_if_admin(self):
        """Check if admin can add users"""

        url = reverse('user-list')
        self.client.login(username='admin', password='test12345')
        response = self.client.post(url, self.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)

    def test_post_user_if_regular_user(self):
        """Check if POST user returns 403 status if user is not admin"""

        url = reverse('user-list')
        self.client.login(username='test', password='test54321')
        response = self.client.post(url, self.data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(User.objects.count(), 2)

    def test_post_user_if_anonymous(self):
        """Check if POST user returns 403 status if user is anonymous"""

        url = reverse('user-list')
        response = self.client.post(url, self.data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(User.objects.count(), 2)
