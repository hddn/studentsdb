from datetime import datetime

from django.test import TestCase, Client
from django.core.urlresolvers import reverse

from students.models import Group, Student


class TestStudentsList(TestCase):
    """Test for StudentsList view"""

    @classmethod
    def setUpTestData(cls):
        group1 = Group.objects.create(id=1, title='Group1')
        group2 = Group.objects.create(id=2, title='Group2')

        Student.objects.create(id=1, first_name='Michael', last_name='Jordan',
                               birthday=datetime.now(), ticket='23', student_group=group1)
        Student.objects.create(id=2, first_name='Kobe', last_name='Bryant',
                               birthday=datetime.now(), ticket='24', student_group=group1)
        Student.objects.create(id=3, first_name='Vince', last_name='Carter',
                               birthday=datetime.now(), ticket='15', student_group=group1)
        Student.objects.create(id=4, first_name='LeBron', last_name='James',
                               birthday=datetime.now(), ticket='6', student_group=group2)

    def setUp(self):
        self.client = Client()
        self.url = reverse('home')

    def test_student_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        # check if student is in the list
        self.assertIn(b'Jordan', response.content)

        # check if student edit link is in the response
        self.assertIn(reverse('students_edit', kwargs={'pk': Student.objects.all()[0].id}).encode(), response.content)

        # check for pagination
        self.assertEqual(len(response.context['students']), 3)
        response = self.client.get(self.url, {'page': '2'})
        self.assertEqual(len(response.context['students']), 1)

    def test_order_by(self):
        response = self.client.get(self.url, {'order_by': 'last_name'})
        students = response.context['students']

        self.assertEqual(students[0].last_name, 'Bryant')
        self.assertEqual(students[1].last_name, 'Carter')
        self.assertEqual(students[2].last_name, 'James')

        # test reversed order
        response = self.client.get(self.url, {'order_by': 'last_name', 'reverse': '1'})
        students = response.context['students']

        self.assertEqual(students[0].last_name, 'Jordan')
        self.assertEqual(students[1].last_name, 'James')
        self.assertEqual(students[2].last_name, 'Carter')

    def test_current_group(self):
        group = Group.objects.get(pk=2)
        self.client.cookies['current_group'] = group.id
        response = self.client.get(self.url)
        self.assertEqual(len(response.context['students']), 1)
