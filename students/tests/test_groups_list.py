from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.core.urlresolvers import reverse

from students.models import Group


class TestGroupsList(TestCase):
    """Test for GroupsList view"""

    @classmethod
    def setUpTestData(cls):
        # TODO: use mocks
        Group.objects.create(id=1, title='Group4')
        Group.objects.create(id=2, title='Group2')
        Group.objects.create(id=3, title='Group1')
        Group.objects.create(id=4, title='Group3')

        User.objects.create_user(id=1, username='admin', password='test12345', email='admin@admin.com')

    def setUp(self):
        self.client = Client()

        # we must log in as admin to access Groups page
        self.client.login(username='admin', password='test12345')
        self.url = reverse('groups')

    def test_groups_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        # check if group is in the list
        self.assertIn(b'Group3', response.content)

        # check if group edit link is in the response
        self.assertIn(reverse('groups_edit', kwargs={'pk': Group.objects.all()[0].id}).encode(), response.content)

        # check for pagination
        self.assertEqual(len(response.context['groups']), 3)
        response = self.client.get(self.url, {'page': '2'})
        self.assertEqual(len(response.context['groups']), 1)

    def test_order_by(self):
        response = self.client.get(self.url, {'order_by': 'title'})
        groups = response.context['groups']

        self.assertEqual(groups[0].title, 'Group1')
        self.assertEqual(groups[1].title, 'Group2')
        self.assertEqual(groups[2].title, 'Group3')

        # test reversed order
        response = self.client.get(self.url, {'order_by': 'title', 'reverse': '1'})
        groups = response.context['groups']

        self.assertEqual(groups[0].title, 'Group4')
        self.assertEqual(groups[1].title, 'Group3')
        self.assertEqual(groups[2].title, 'Group2')

    def test_current_group(self):
        group = Group.objects.get(pk=2)
        self.client.cookies['current_group'] = group.id
        response = self.client.get(self.url)
        self.assertEqual(len(response.context['groups']), 1)

    def test_access(self):
        # try to access view as anonymous user
        self.client.logout()
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)

        # we have to get a login form
        self.assertIn(b'Login Form', response.content)

        # check for redirect
        self.assertEqual(response.redirect_chain[0], ('/users/login/?next=/groups/', 302))
