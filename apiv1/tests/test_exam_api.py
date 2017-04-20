from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from students.models import Exam


class ExamAPITestCase(APITestCase):
    """Test for exam api"""

    def setUp(self):
        User.objects.create_user(username='admin', password='test12345', email='admin@admin.com')

        self.exam = Exam.objects.create(subject='Test', date=timezone.now())
        self.data = {'subject': 'Some Exam',
                     'date': timezone.now()}

    def test_exams_list_if_anonymous(self):
        """Check if GET exams returns 403 status if user is anonymous"""

        url = reverse('exam-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_exams_list_if_authenticated(self):
        """Check if logged in user can get a exams list"""

        url = reverse('exam-list')
        self.client.login(username='admin', password='test12345')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['results']), 1)

    def test_get_exam_if_anonymous(self):
        """Check if GET exam detail returns 403 status if user is anonymous"""

        url = reverse('exam-detail', args=[self.exam.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_exam_if_authenticated(self):
        """Check if logged in user can add exams"""

        url = reverse('exam-list')
        self.client.login(username='admin', password='test12345')
        response = self.client.post(url, self.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Exam.objects.count(), 2)

    def test_post_exam_if_anonymous(self):
        """Check if POST exam returns 403 status if user is anonymous"""

        url = reverse('exam-list')
        response = self.client.post(url, self.data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Exam.objects.count(), 1)
