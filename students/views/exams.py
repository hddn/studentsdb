# -*- coding: utf-8 -*-

from django.views.generic import ListView

from students.models import Exam
from students.util import get_current_group

EXAMS_NUM = 3  # number of exams for pagination


class ExamsListView(ListView):
    template_name = 'students/exams.html'
    model = Exam
    paginate_by = EXAMS_NUM
    context_object_name = 'exams'

    def get_queryset(self):
        current_group = get_current_group(self.request)
        if current_group:
            queryset = Exam.objects.filter(group=current_group)
        else:
            queryset = Exam.objects.all()
        order_by = self.request.GET.get('order_by', '')
        if order_by in ('subject', 'teacher', 'group', 'date'):
            queryset = queryset.order_by(order_by)
            if self.request.GET.get('reverse', '') == '1':
                queryset = queryset.reverse()
        return queryset
