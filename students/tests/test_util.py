from datetime import datetime

from django.http import HttpRequest
from django.test import TestCase

from students.models import Group, Student
from students.util import get_current_group, get_groups, paginate


class UtilsTestCase(TestCase):
    """Test functions from util module"""

    @classmethod
    def setUpTestData(cls):
        group = Group.objects.create(id=1, title='Group1')
        group2 = Group.objects.create(id=2, title='Group2')
        student = Student.objects.create(id=1, first_name='Michael', last_name='Jordan',
                                         birthday=datetime.now(), ticket='23')

        group.leader = student
        group.save()

    def setUp(self):
        self.request = HttpRequest()

    def test_get_current_group(self):
        self.request.COOKIES['current_group'] = ''
        self.assertEqual(get_current_group(self.request), None)

        self.request.COOKIES['current_group'] = '1234567'
        self.assertEqual(get_current_group(self.request), None)

        group = Group.objects.get(pk=1)
        self.request.COOKIES['current_group'] = str(group.pk)
        self.assertEqual(get_current_group(self.request), group)

    def test_get_groups(self):
        self.request.COOKIES['current_group'] = '2'
        self.assertEqual(len(get_groups(self.request)), 2)
        self.assertEqual(get_groups(self.request), [
            {'id': 1,
             'title': 'Group1',
             'leader': 'Michael Jordan',
             'selected': False},
            {'id': 2,
             'title': 'Group2',
             'leader': None,
             'selected': True}
        ])

    def test_paginate(self):
        self.request.GET['page'] = 'test'
        context = paginate([1, 2, 3], 2, self.request, {})
        self.assertEqual(len(context['object_list']), 2)
        self.assertEqual(len(context['page_obj']), 2)
        self.assertEqual(context['is_paginated'], True)
        self.assertEqual(context['object_list'][0], 1)
        self.assertEqual(context['object_list'][1], 2)

        self.request.GET['page'] = '999'
        context = paginate([1, 2, 3], 2, self.request, {})
        self.assertEqual(len(context['object_list']), 1)
        self.assertEqual(len(context['page_obj']), 1)
        self.assertEqual(context['is_paginated'], True)
        self.assertEqual(context['object_list'][0], 3)

        self.request.GET['page'] = '2'
        context = paginate([1, 2, 3], 2, self.request, {})
        self.assertEqual(len(context['object_list']), 1)
        self.assertEqual(len(context['page_obj']), 1)
        self.assertEqual(context['is_paginated'], True)
        self.assertEqual(context['object_list'][0], 3)
