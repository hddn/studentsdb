from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.utils import timezone

from students.models import Exam, Group


class TestExamsList(TestCase):
    """Test for ExamsList view"""

    @classmethod
    def setUpTestData(cls):
        group = Group.objects.create(id=1, title='Group4')
        Exam.objects.create(id=1, subject='Exam1', date=timezone.now(), group=group)
        Exam.objects.create(id=2, subject='Exam2', date=timezone.now())
        Exam.objects.create(id=3, subject='Exam3', date=timezone.now())
        Exam.objects.create(id=4, subject='Exam4', date=timezone.now())

        User.objects.create_user(id=1, username='admin', password='test12345', email='admin@admin.com')

    def setUp(self):
        self.client = Client()

        # we must log in as admin to access Exams page
        self.client.login(username='admin', password='test12345')
        self.url = reverse('exams')

    def test_exams_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        # check if exam is in the list
        self.assertIn(b'Exam2', response.content)

        # check for pagination
        self.assertEqual(len(response.context['exams']), 3)
        response = self.client.get(self.url, {'page': '2'})
        self.assertEqual(len(response.context['exams']), 1)

    def test_order_by(self):
        response = self.client.get(self.url, {'order_by': 'date'})
        exams = response.context['exams']

        self.assertEqual(exams[0].subject, 'Exam1')
        self.assertEqual(exams[1].subject, 'Exam2')
        self.assertEqual(exams[2].subject, 'Exam3')

        # test reversed order
        response = self.client.get(self.url, {'order_by': 'date', 'reverse': '1'})
        exams = response.context['exams']

        self.assertEqual(exams[0].subject, 'Exam4')
        self.assertEqual(exams[1].subject, 'Exam3')
        self.assertEqual(exams[2].subject, 'Exam2')

    def test_current_group(self):
        group = Group.objects.get(pk=1)
        self.client.cookies['current_group'] = group.id
        response = self.client.get(self.url)
        self.assertEqual(len(response.context['exams']), 1)

    def test_access(self):
        # try to access view as anonymous user
        self.client.logout()
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)

        # we have to get a login form
        self.assertIn(b'Login Form', response.content)

        # check for redirect
        self.assertEqual(response.redirect_chain[0], ('/users/login/?next=/exams/', 302))
