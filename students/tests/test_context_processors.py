from django.http import HttpRequest
from django.test import TestCase

from students.context_processors import groups_processor
from students.models import Group


class TestContextProcessor(TestCase):
    """Test for groups processor"""

    @classmethod
    def setUpTestData(cls):
        Group.objects.create(id=1, title='Group1')
        Group.objects.create(id=2, title='Group2')

    def test_groups_processor(self):
        request = HttpRequest()
        context = groups_processor(request)

        self.assertEqual(len(context['GROUPS']), 2)
        self.assertEqual(context['GROUPS'][0]['title'], 'Group1')
        self.assertEqual(context['GROUPS'][1]['title'], 'Group2')
