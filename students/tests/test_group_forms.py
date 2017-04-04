from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from students.models import Group


class TestGroupUpdateForm(TestCase):
    """Test for GroupEdit form"""

    @classmethod
    def setUpTestData(cls):
        Group.objects.create(id=1, title='Group1')
        User.objects.create_user(id=1, username='admin', password='test12345', email='admin@admin.com')

    def setUp(self):
        self.client = Client()
        self.url = reverse('groups_edit', kwargs={'pk': 1})
        self.home_url = reverse('groups')

        # log in as admin
        self.client.login(username='admin', password='test12345')

    def test_form(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        self.assertIn(b'Edit Group', response.content)
        self.assertIn(b'Title', response.content)
        self.assertIn(b'name="add_button"', response.content)
        self.assertIn(b'name="cancel_button"', response.content)
        self.assertIn(b'action="%b"' % self.url.encode(), response.content)

        # test cancel button
        response = self.client.post(self.url, {'cancel_button': 'Cancel'}, follow=True)
        self.assertEqual(response.redirect_chain[0][0], self.home_url)

    def test_update_success(self):
        # post form with data
        response = self.client.post(self.url, {'title': 'Test Title', 'leader': ''}, follow=True)
        self.assertEqual(response.status_code, 200)

        # test updated details
        group = Group.objects.get(pk=1)
        self.assertEqual(group.title, 'Test Title')
        self.assertEqual(group.leader, None)

        # check for proper redirect
        self.assertIn(b'Group update successful!', response.content)
        self.assertEqual(response.redirect_chain[0][0], self.home_url)

    def test_access(self):
        # try to access form as anonymous user
        self.client.logout()
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)

        # we have to get a login form
        self.assertIn(b'Login Form', response.content)

        # check for redirect
        self.assertEqual(response.redirect_chain[0], ('/users/login/?next=/groups/1/edit/', 302))
