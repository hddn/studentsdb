
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.views.generic import UpdateView, DeleteView, CreateView

from ..models import Group
from ..forms import GroupEditForm
from ..util import paginate, get_current_group
# Create your views here.


def groups_list(request):
    current_group = get_current_group(request)
    if current_group:
        groups = Group.objects.filter(title=current_group.title)
    else:
        groups = Group.objects.all()

    order_by = request.GET.get('order_by', '')
    if order_by in ('title', 'leader'):
        groups = groups.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            groups = groups.reverse()

    context = paginate(groups, 3, request, {}, var_name='groups')
    
    return render(request, 'students/groups.html', context)


class GroupUpdateView(UpdateView):
    model = Group
    template_name = 'students/groups_edit.html'
    form_class = GroupEditForm

    def get_success_url(self):
        return '%s?status_message=%s' % (reverse('home'), _('Group saved'))

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect('%s?status_message=%s' % (reverse('home'), _('Canceled')))
        else:
            return super(GroupUpdateView, self).post(request, *args, **kwargs)


class GroupAddView(CreateView):
    model = Group
    template_name = 'students/groups_add.html'
    form_class = GroupEditForm

    def get_success_url(self):
        return '%s?status_message=%s' % (reverse('home'), _('Group added'))

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect('%s?status_message=%s' % (reverse('home'), _('Canceled')))
        else:
            return super(GroupAddView, self).post(request, *args, **kwargs)


class GroupDeleteView(DeleteView):
    model = Group
    template_name = 'students/groups_confirm_delete.html'
    
    def get_success_url(self):
        return '%s?status_message=%s' % (reverse('home'), _('Group deleted'))
