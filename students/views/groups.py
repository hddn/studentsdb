# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.forms import ModelForm
from django.views.generic import UpdateView, DeleteView, CreateView

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from crispy_forms.bootstrap import FormActions

from ..models.group import Group
# Create your views here.


def groups_list(request):
    groups = Group.objects.all()

    order_by = request.GET.get('order_by', '')
    if order_by in ('title', 'leader'):
        groups = groups.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            groups = groups.reverse()

    paginator = Paginator(groups, 3)
    page = request.GET.get('page')
    try:
        groups = paginator.page(page)
    except PageNotAnInteger:
        groups = paginator.page(1)
    except EmptyPage:
        groups = paginator.page(paginator.num_pages)
    
    return render(request, 'students/groups.html', {'groups': groups})


class GroupEditForm(ModelForm):
    
    class Meta:
        model = Group
        fields = ['title', 'leader', 'notes']

    def __init__(self, *args, **kwargs):
        super(GroupEditForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        if kwargs['instance'] is None:
            add_form = True
        else:
            add_form = False

        if add_form:
            self.helper.action = reverse('groups_add')
        else:
            self.helper.action = reverse('groups_edit',
                                         kwargs={'pk': kwargs['instance'].id})

        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        self.helper.help_text_inline = True
        self.helper.html5_required = False

        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'

        self.helper.layout = Layout(
            self.helper.layout, FormActions(
                Submit('add_button', u'Зберегти', css_class="btn btn-primary"),
                Submit('cancel_button', u'Скасувати', css_class="btn btn-link"),
            ))

class GroupUpdateView(UpdateView):
    model = Group
    template_name = 'students/groups_edit.html'
    form_class = GroupEditForm

    def get_success_url(self):
        return u'%s?status_message=Групу збережено' % reverse('home')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(
                u'%s?status_message=Редагування скасовано' % reverse('home'))
        else:
            return super(GroupUpdateView, self).post(request, *args, **kwargs)


class GroupAddView(CreateView):
    model = Group
    template_name = 'students/groups_add.html'
    form_class = GroupEditForm

    def get_success_url(self):
        return u'%s?status_message=Групу збережено' % reverse('home')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(
                u'%s?status_message=Додавання скасовано' % reverse('home'))
        else:
            return super(GroupAddView, self).post(request, *args, **kwargs)


class GroupDeleteView(DeleteView):
    model = Group
    template_name = 'students/groups_confirm_delete.html'
    
    def get_success_url(self):
        return u'%s?status_message=Групу видалено' % reverse('home')