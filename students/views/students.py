from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.translation import ugettext as _
from django.views.generic import ListView, UpdateView, DeleteView, CreateView

from braces.views import FormValidMessageMixin

from students.models import Student
from students.forms import StudentEditForm
from students.util import get_current_group

STUDENTS_NUM = 3  # number of students for pagination


class StudentUpdateView(FormValidMessageMixin, UpdateView):
    model = Student
    template_name = 'students/students_edit.html'
    form_class = StudentEditForm
    success_url = reverse_lazy('home')
    form_valid_message = _('Student updated successfully!')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(reverse('home'))
        else:
            return super(StudentUpdateView, self).post(request, *args, **kwargs)


class StudentAddView(FormValidMessageMixin, CreateView):
    model = Student
    template_name = 'students/students_add.html'
    form_class = StudentEditForm
    success_url = reverse_lazy('home')
    form_valid_message = _('Student added successfully!')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(reverse('home'))
        else:
            return super(StudentAddView, self).post(request, *args, **kwargs)


class StudentDeleteView(FormValidMessageMixin, DeleteView):
    model = Student
    template_name = 'students/students_confirm_delete.html'
    success_url = reverse_lazy('home')

    def get_form_valid_message(self):
        return 'Student {} {} deleted!'.format(self.object.first_name, self.object.last_name)


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
        order_by = self.request.GET.get('order_by', 'id')
        if order_by in ('id', 'last_name', 'first_name', 'ticket'):
            queryset = queryset.order_by(order_by)
            if self.request.GET.get('reverse', '') == '1':
                queryset = queryset.reverse()
        return queryset
