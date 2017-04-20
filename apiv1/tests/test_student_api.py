from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from students.models import Student


class StudentAPITestCase(APITestCase):
    """Test for student api"""

    def setUp(self):
        User.objects.create_user(username='admin', password='test12345', email='admin@admin.com')

        self.student = Student.objects.create(first_name='Michael', last_name='Jordan')
        self.data = {
            'first_name': 'John',
            'last_name': 'Snow'
        }

    def test_students_list(self):
        """Check if anonymous user can get a students list"""

        url = reverse('student-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['results']), 1)

    def test_get_student(self):
        """Check if anonymous user can get a student detail"""

        url = reverse('student-detail', args=[self.student.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['first_name'], 'Michael')
        self.assertEqual(response.json()['last_name'], 'Jordan')

    def test_post_student_if_authenticated(self):
        """Check if logged in user can add students"""

        url = reverse('student-list')
        self.client.login(username='admin', password='test12345')
        response = self.client.post(url, self.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Student.objects.count(), 2)

    def test_post_student_if_anonymous(self):
        """Check if POST student returns 403 status if user is anonymous"""

        url = reverse('student-list')
        response = self.client.post(url, self.data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Student.objects.count(), 1)
