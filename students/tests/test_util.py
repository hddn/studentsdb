from datetime import datetime

from django.http import HttpRequest
from django.test import TestCase

from students.models import Group, Student
from students.util import get_current_group, get_groups, paginate


class UtilsTestCase(TestCase):
    """Tests for functions from util module"""

    def setUp(self):
        # create test objects
        # TODO: use mocks
        group, created = Group.objects.get_or_create(id=1, title='Group1')
        group2, created = Group.objects.get_or_create(id=2, title='Group2')
        student, created = Student.objects.get_or_create(id=1, first_name='Michael', last_name='Jordan',
                                                         birthday=datetime.now(), ticket='23')

        group.leader = student
        group.save()

    def test_get_current_group(self):
        # prepare request object for utility function
        request = HttpRequest()

        # test with no current group set in cookie
        request.COOKIES['current_group'] = ''
        self.assertEqual(get_current_group(request), None)

        # test with invalid id
        request.COOKIES['current_group'] = '1234567'
        self.assertEqual(get_current_group(request), None)

        # test with valid group id
        group = Group.objects.get(pk=1)
        request.COOKIES['current_group'] = str(group.pk)
        self.assertEqual(get_current_group(request), group)

    def test_get_groups(self):
        # prepare request object
        request = HttpRequest()

        # set current group cookie
        request.COOKIES['current_group'] = '2'

        # check if group list is not empty
        self.assertEqual(len(get_groups(request)), 2)

        # test with valid JSON
        self.assertEqual(get_groups(request), [
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
        # prepare request object
        request = HttpRequest()

        # test with not integer page
        request.GET['page'] = 'test'
        context = paginate([1, 2, 3], 2, request, {})
        self.assertEqual(len(context['object_list']), 2)
        self.assertEqual(len(context['page_obj']), 2)
        self.assertEqual(context['is_paginated'], True)
        self.assertEqual(context['object_list'][0], 1)
        self.assertEqual(context['object_list'][1], 2)

        # test with empty page
        request.GET['page'] = '999'
        context = paginate([1, 2, 3], 2, request, {})
        self.assertEqual(len(context['object_list']), 1)
        self.assertEqual(len(context['page_obj']), 1)
        self.assertEqual(context['is_paginated'], True)
        self.assertEqual(context['object_list'][0], 3)

        # test with valid page(2)
        request.GET['page'] = '2'
        context = paginate([1, 2, 3], 2, request, {})
        self.assertEqual(len(context['object_list']), 1)
        self.assertEqual(len(context['page_obj']), 1)
        self.assertEqual(context['is_paginated'], True)
        self.assertEqual(context['object_list'][0], 3)
