
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.views.generic import UpdateView, DeleteView, CreateView

from ..models import Student
from ..forms import StudentEditForm
from ..util import paginate, get_current_group

#from django.utils.decorators import method_decorator
#from django.contrib.auth.decorators import login_required

# Create your views here.



class StudentUpdateView(UpdateView):
    model = Student
    template_name = 'students/students_edit.html'
    form_class = StudentEditForm
    
    def get_success_url(self):
        return u'%s?status_message=%s' % (reverse('home'),
                                          _(u'Student updated successfully!'))

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(
                u'%s?status_message=%s' % (reverse('home'),
                                           _(u'Student updating canceled')))
        else:
            return super(StudentUpdateView, self).post(request, *args, **kwargs)

    
class StudentAddView(CreateView):
    model = Student
    template_name = 'students/students_add.html'
    form_class = StudentEditForm

    def get_success_url(self):
        return u'%s?status_message=%s' % (reverse('home'),
                                          _(u'Student added successfully!'))

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(
                u'%s?status_message=%s' % (reverse('home'),
                                           _(u'Student adding canceled')))
        else:
            return super(StudentAddView, self).post(request, *args, **kwargs)


class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'students/students_confirm_delete.html'

    def get_success_url(self):
        return u'%s?status_message=%s' % (reverse('home'),
                                          _(u'Student deleted'))


def students_list(request):
    current_group = get_current_group(request)
    if current_group:
        students = Student.objects.filter(student_group=current_group)
    else:
        students = Student.objects.all()

    order_by = request.GET.get('order_by', '')
    if order_by in ('last_name', 'first_name', 'ticket'):
        students = students.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            students = students.reverse()

    context = paginate(students, 3, request, {}, var_name='students')
    
    return render(request, 'students/students_list.html', context)