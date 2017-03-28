import logging
from django.test import TestCase
from django.utils.six import StringIO

from students.models import Student


class SignalsTests(TestCase):
    """Test for Student signals"""

    def setUp(self):
        self.out = StringIO()
        self.handler = logging.StreamHandler(self.out)
        logging.root.addHandler(self.handler)

        Student.objects.create(id=1, first_name='Test', last_name='Student')

    def test_updated_added_event(self):
        # check if add signal message is in the output file
        self.out.seek(0)
        student = Student.objects.get(pk=1)
        self.assertEqual(self.out.readlines()[-1], 'Student added: Test Student (ID: {:d})\n'.format(student.id))

        # check if update signal message is in the output file
        student.ticket = '123'
        student.save()
        self.out.seek(0)
        self.assertEqual(self.out.readlines()[-1], 'Student updated: Test Student (ID: {:d})\n'.format(student.id))

    def test_deleted_event(self):
        student = Student.objects.get(pk=1)
        pk = student.id
        student.delete()
        self.out.seek(0)
        self.assertEqual(self.out.readlines()[-1], 'Student deleted: Test Student (ID: {:d})\n'.format(pk))

    def tearDown(self):
        # remove our handler from root logger
        logging.root.removeHandler(self.handler)
