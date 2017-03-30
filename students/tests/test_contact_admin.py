from django.contrib.auth.models import User
from django.core import mail
from django.test import Client, TestCase
from django.urls import reverse


class ContactAdminTest(TestCase):
    """Test for Contact Admin form"""

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(id=1, username='admin', password='test12345', email='admin@admin.com')

    def test_email_sending(self):
        client = Client()
        client.login(username='admin', password='test12345')
        client.post(reverse('contact_admin'), {
            'from_email': 'test@test.com',
            'subject': 'test email',
            'message': 'test message'
        })

        # check if email backend caught our message
        msg = mail.outbox[0].message()
        self.assertEqual(msg.get('subject'), 'test email')
        self.assertEqual(msg.get('From'), 'test@test.com')
        self.assertEqual(msg.get_payload(), 'test message')
