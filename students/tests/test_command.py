from datetime import datetime

from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase
from django.utils.six import StringIO

from students.models import Group, Student


class STCountTest(TestCase):
    """Test for stcount custom command"""

    @classmethod
    def setUpTestData(cls):
        group1 = Group.objects.create(id=1, title='Group1')
        group2 = Group.objects.create(id=2, title='Group2')

        Student.objects.create(id=1, first_name='Michael', last_name='Jordan',
                               birthday=datetime.now(), ticket='23', student_group=group1)
        Student.objects.create(id=2, first_name='Kobe', last_name='Bryant',
                               birthday=datetime.now(), ticket='24', student_group=group1)
        User.objects.create_user(id=1, username='admin', password='test12345', email='admin@admin.com')

    def test_output(self):
        out = StringIO()
        call_command('stcount', 'student', 'group', 'user', stdout=out)
        result = out.getvalue()

        # check if we get proper number of objects
        self.assertIn('students in database: 2', result)
        self.assertIn('groups in database: 2', result)
        self.assertIn('users in database: 1', result)
