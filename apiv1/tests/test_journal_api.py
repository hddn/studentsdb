from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from students.models import MonthJournal, Student


class JournalAPITestCase(APITestCase):
    """Test for journal api"""

    def setUp(self):
        User.objects.create_user(username='admin', password='test12345', email='admin@admin.com')
        student = Student.objects.create(first_name='Michael', last_name='Jordan')
        new_student = Student.objects.create(first_name='Kobe', last_name='Bryant')

        self.journal = MonthJournal.objects.create(student=student, date='2017-11-11')
        self.data = {'student': new_student.pk,
                     'date': '2017-10-10'}

    def test_journals_list_if_anonymous(self):
        """Check if GET journals returns 403 status if user is anonymous"""

        url = reverse('monthjournal-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_journals_list_if_authenticated(self):
        """Check if logged in user can get a journals list"""

        url = reverse('monthjournal-list')
        self.client.login(username='admin', password='test12345')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['results']), 1)

    def test_get_journal_if_anonymous(self):
        """Check if GET journal detail returns 403 status if user is anonymous"""

        url = reverse('monthjournal-detail', args=[self.journal.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_journal_if_authenticated(self):
        """Check if logged in user can add journals"""

        url = reverse('monthjournal-list')
        self.client.login(username='admin', password='test12345')
        response = self.client.post(url, self.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MonthJournal.objects.count(), 2)

    def test_post_journal_if_anonymous(self):
        """Check if POST journal returns 403 status if user is anonymous"""

        url = reverse('monthjournal-list')
        response = self.client.post(url, self.data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(MonthJournal.objects.count(), 1)
