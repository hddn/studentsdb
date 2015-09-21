# -*- coding: utf-8 -*-

from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from ..models.student import Student
from ..models.group import Group

from django.forms import ModelForm
from django.views.generic import UpdateView, DeleteView, CreateView

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from crispy_forms.bootstrap import FormActions

# Create your views here.


class StudentUpdateForm(ModelForm):

    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'middle_name',
                  'birthday', 'photo', 'ticket',
                  'student_group', 'notes']

    def __init__(self, *args, **kwargs):
        super(StudentUpdateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.form_action = reverse('students_edit',
                                          kwargs={'pk': kwargs['instance'].id})
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'

        self.helper.layout = Layout(
            self.helper.layout, FormActions(
                Submit('add_button', u'Зберегти', css_class="btn btn-primary"),
                Submit(
                    'cancel_button', u'Скасувати', css_class="btn btn-link"),
            ))


class StudentAddForm(ModelForm):

    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'middle_name',
                  'birthday', 'photo', 'ticket',
                  'student_group', 'notes']

    def __init__(self, *args, **kwargs):
        super(StudentAddForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.form_action = reverse('students_add')
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'

        self.helper.layout = Layout(
            self.helper.layout, FormActions(
                Submit('add_button', u'Зберегти', css_class="btn btn-primary"),
                Submit(
                    'cancel_button', u'Скасувати', css_class="btn btn-link"),
            ))       
        

class StudentUpdateView(UpdateView):

    model = Student
    template_name = 'students/students_edit.html'
    form_class = StudentUpdateForm
    # fields = ['first_name', 'last_name', 'middle_name',
    #          'birthday', 'photo', 'ticket', 'student_group']

    def get_success_url(self):
        return u'%s?status_message=Студента успішно збережено!' % reverse('home')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(
                u'%s?status_message=Редагування студента відмінено!' %
                reverse('home'))
        else:
            return super(StudentUpdateView, self).post(request, *args, **kwargs)


class StudentAddView(CreateView):
    model = Student
    template_name = 'students/students_add.html'
    form_class = StudentAddForm

    def get_success_url(self):
        return u'%s?status_message=Студента успішно збережено!' % reverse('home')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(
                u'%s?status_message=Додавання студента відмінено!' %
                reverse('home'))
        else:
            return super(StudentAddView, self).post(request, *args, **kwargs)


class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'students/students_confirm_delete.html'

    def get_success_url(self):
        return u'%s?status_message=Студента видалено' % reverse('home')


def students_list(request):
    students = Student.objects.all()

    order_by = request.GET.get('order_by', '')
    if order_by in ('last_name', 'first_name', 'ticket'):
        students = students.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            students = students.reverse()

    paginator = Paginator(students, 3)
    page = request.GET.get('page')
    try:
        students = paginator.page(page)
    except PageNotAnInteger:
        students = paginator.page(1)
    except EmptyPage:
        students = paginator.page(paginator.num_pages)

    return render(request, 'students/students_list.html', {'students': students})