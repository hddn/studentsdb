from django.http import HttpRequest
from django.test import TestCase

from studentsdb.context_processors import student_proc
from studentsdb.settings import PORTAL_URL


class TestContextProcessor(TestCase):
    """Test for portal url processor"""

    def test_portal_url(self):
        request = HttpRequest()
        context = student_proc(request)

        self.assertEqual(context['PORTAL_URL'], PORTAL_URL)
