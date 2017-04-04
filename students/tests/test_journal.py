from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.core.urlresolvers import reverse

from students.models import Student, Group


class TestJournal(TestCase):
    """Test for MonthJournal view"""

    @classmethod
    def setUpTestData(cls):
        group = Group.objects.create(id=1, title='Group1')
        Student.objects.create(id=1, first_name='Michael', last_name='Jordan',
                               birthday=datetime.now(), ticket='23', student_group=group)
        Student.objects.create(id=2, first_name='Kobe', last_name='Bryant',
                               birthday=datetime.now(), ticket='24')
        User.objects.create_user(id=1, username='admin', password='test12345', email='admin@admin.com')

    def setUp(self):
        self.client = Client()

        # we must log in as admin to access Journal page
        self.client.login(username='admin', password='test12345')
        self.url = reverse('journal')

    def test_journal(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        # check if student is in the list
        self.assertIn(b'Bryant', response.content)

        # check if all students are on the page
        self.assertEqual(len(response.context['students']), 2)

        # post some data
        student = Student.objects.get(pk=1)
        response = self.client.post(self.url, {'date': datetime.now().date(),
                                               'present': datetime.now().date(),
                                               'pk': student.id})
        self.assertEqual(response.content, b'{"status": "success"}')

    def test_current_group(self):
        group = Group.objects.get(pk=1)
        self.client.cookies['current_group'] = group.id
        response = self.client.get(self.url)
        self.assertEqual(len(response.context['students']), 1)

    def test_access(self):
        # try to access view as anonymous user
        self.client.logout()
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)

        # we have to get a login form
        self.assertIn(b'Login Form', response.content)

        # check for redirect
        self.assertEqual(response.redirect_chain[0], ('/users/login/?next=/journal/', 302))
