from datetime import datetime

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from students.models import Group, Student


class TestStudentUpdateForm(TestCase):
    """Test for StudentEdit form"""

    @classmethod
    def setUpTestData(cls):
        group1 = Group.objects.create(id=1, title='Group1')
        group2 = Group.objects.create(id=2, title='Group2')

        Student.objects.create(id=1, first_name='Michael', last_name='Jordan',
                               birthday=datetime.now(), ticket='23', student_group=group1)
        Student.objects.create(id=2, first_name='Kobe', last_name='Bryant',
                               birthday=datetime.now(), ticket='24', student_group=group1)
        User.objects.create_user(id=1, username='admin', password='test12345', email='admin@admin.com')

    def setUp(self):
        self.client = Client()
        self.url = reverse('students_edit', kwargs={'pk': 1})
        self.home_url = reverse('home')

    def test_form(self):
        # login as admin
        self.client.login(username='admin', password='test12345')

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        self.assertIn(b'Edit Student', response.content)
        self.assertIn(b'Last Name', response.content)
        self.assertIn(b'name="add_button"', response.content)
        self.assertIn(b'name="cancel_button"', response.content)
        self.assertIn(b'action="%b"' % self.url.encode(), response.content)

        # test cancel button
        response = self.client.post(self.url, {'cancel_button': 'Cancel'}, follow=True)
        self.assertEqual(response.redirect_chain[0][0], self.home_url)

    def test_update_success(self):
        self.client.login(username='admin', password='test12345')

        # post form with data
        group = Group.objects.get(pk=1)
        response = self.client.post(self.url, {
            'first_name': 'Test Name',
            'last_name': 'Test Last Name',
            'ticket': '123',
            'student_group': group.id,
            'birthday': '1999-11-12'
        }, follow=True)
        self.assertEqual(response.status_code, 200)

        # test updated details
        student = Student.objects.get(pk=1)
        self.assertEqual(student.first_name, 'Test Name')
        self.assertEqual(student.last_name, 'Test Last Name')
        self.assertEqual(student.ticket, '123')
        self.assertEqual(student.student_group, group)

        # check for proper redirect
        self.assertIn(b'Student updated successfully', response.content)
        self.assertEqual(response.redirect_chain[0][0], self.home_url)

    def test_access(self):
        # try to access form as anonymous user
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)

        # we have to get a login form
        self.assertIn(b'Login Form', response.content)

        # check for redirect
        self.assertEqual(response.redirect_chain[0], ('/users/login/?next=/students/1/edit/', 302))
