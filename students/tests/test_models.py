from datetime import datetime

from django.test import TestCase

from students.models import Student, Group, Exam, MonthJournal


class TestStudentModel(TestCase):
    """Test for Student model"""

    def test_str(self):
        student = Student(first_name='Test', last_name='Student')
        self.assertEqual(str(student), 'Test Student')


class TestGroupModel(TestCase):
    """Test for Group model"""

    def test_str(self):
        group = Group(title='Some Title')
        self.assertEqual(str(group), 'Some Title')

        student = Student(id=1, first_name='Test', last_name='Student')
        group2 = Group(title='Another Title', leader=student)
        self.assertEqual(str(group2), 'Another Title (Test Student)')


class TestExamModel(TestCase):
    """Test for Exam model"""

    def test_str(self):
        exam = Exam(subject='Test', date='2017-11-11')
        self.assertEqual(str(exam), 'Test (2017-11-11)')

        group = Group(title='Some Title')
        exam2 = Exam(subject='Test2', group=group, date='2017-10-10')
        self.assertEqual(str(exam2), 'Some Title, Test2 (2017-10-10)')


class TestJournalModel(TestCase):
    """Test for MonthJournal model"""

    def test_str(self):
        student = Student(first_name='Test', last_name='Student')
        journal = MonthJournal(student=student, date=datetime(2017, 10, 10))
        self.assertEqual(str(journal), 'Student: 10, 2017')
