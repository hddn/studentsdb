from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from students.models import Group


class GroupAPITestCase(APITestCase):
    """Test for group api"""

    def setUp(self):
        User.objects.create_user(username='admin', password='test12345', email='admin@admin.com')

        self.group = Group.objects.create(title='Test')
        self.data = {'title': 'Some Group'}

    def test_groups_list_if_anonymous(self):
        """Check if anonymous user can get a groups list"""

        url = reverse('group-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_groups_list_if_authenticated(self):
        """Check if logged in user can get a groups list"""

        url = reverse('group-list')
        self.client.login(username='admin', password='test12345')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['results']), 1)

    def test_get_group_if_anonymous(self):
        """Check if anonymous user can get a group detail"""

        url = reverse('group-detail', args=[self.group.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_group_if_authenticated(self):
        """Check if logged in user can add groups"""

        url = reverse('group-list')
        self.client.login(username='admin', password='test12345')
        response = self.client.post(url, self.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Group.objects.count(), 2)

    def test_post_group_if_anonymous(self):
        """Check if POST group returns 403 status if user is anonymous"""

        url = reverse('group-list')
        response = self.client.post(url, self.data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Group.objects.count(), 1)
