from django.contrib.auth.models import User
from django.test import TestCase

from studentsdb.models import UserProfile


class TestUserProfile(TestCase):
    """Test for UserProfile model"""

    def test_str(self):
        user = User(username='Test', password='test12345')
        user_profile = UserProfile(user=user)

        self.assertEqual(str(user_profile), 'Test')
