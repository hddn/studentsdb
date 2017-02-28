from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.views.generic import ListView, UpdateView, DeleteView, CreateView

from ..models import Student
from ..forms import StudentEditForm
from ..util import get_current_group

STUDENTS_NUM = 5  # number of students for pagination


class StudentUpdateView(UpdateView):
    model = Student
    template_name = 'students/students_edit.html'
    form_class = StudentEditForm
    
    def get_success_url(self):
        return '%s?status_message=%s' % (reverse('home'), _('Student updated successfully!'))

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect('%s?status_message=%s' % (reverse('home'), _('Student updating canceled')))
        else:
            return super(StudentUpdateView, self).post(request, *args, **kwargs)


class StudentAddView(CreateView):
    model = Student
    template_name = 'students/students_add.html'
    form_class = StudentEditForm

    def get_success_url(self):
        return '%s?status_message=%s' % (reverse('home'), _(u'Student added successfully!'))

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect('%s?status_message=%s' % (reverse('home'), _('Student adding canceled')))
        else:
            return super(StudentAddView, self).post(request, *args, **kwargs)


class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'students/students_confirm_delete.html'

    def get_success_url(self):
        return '%s?status_message=%s' % (reverse('home'), _(u'Student deleted'))


class StudentsListView(ListView):
    template_name = 'students/students_list.html'
    model = Student
    paginate_by = STUDENTS_NUM
    context_object_name = 'students'

    def get_queryset(self):
        current_group = get_current_group(self.request)
        if current_group:
            queryset = Student.objects.filter(student_group=current_group)
        else:
            queryset = Student.objects.all()
        order_by = self.request.GET.get('order_by', '')
        if order_by in ('last_name', 'first_name', 'ticket'):
            queryset = queryset.order_by(order_by)
            if self.request.GET.get('reverse', '') == '1':
                queryset = queryset.reverse()
        return queryset
