from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.views.generic import ListView, UpdateView, DeleteView, CreateView

from ..models import Group
from ..forms import GroupEditForm
from ..util import get_current_group

GROUPS_NUM = 5  # number of groups for pagination


class GroupsListView(ListView):
    template_name = 'students/groups.html'
    model = Group
    paginate_by = GROUPS_NUM
    context_object_name = 'groups'

    def get_queryset(self):
        current_group = get_current_group(self.request)
        if current_group:
            queryset = Group.objects.filter(title=current_group.title)
        else:
            queryset = Group.objects.all()
        order_by = self.request.GET.get('order_by', '')
        if order_by in ('title', 'leader'):
            queryset = queryset.order_by(order_by)
            if self.request.GET.get('reverse', '') == '1':
                queryset = queryset.reverse()
        return queryset


class GroupUpdateView(UpdateView):
    model = Group
    template_name = 'students/groups_edit.html'
    form_class = GroupEditForm

    def get_success_url(self):
        return '{}?status_message={}'.format(reverse('groups'), _('Group saved'))

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect('{}?status_message={}'.format(reverse('groups'), _('Canceled')))
        else:
            return super(GroupUpdateView, self).post(request, *args, **kwargs)


class GroupAddView(CreateView):
    model = Group
    template_name = 'students/groups_add.html'
    form_class = GroupEditForm

    def get_success_url(self):
        return '{}?status_message={}'.format(reverse('groups'), _('Group added'))

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect('{}?status_message={}'.format(reverse('groups'), _('Canceled')))
        else:
            return super(GroupAddView, self).post(request, *args, **kwargs)


class GroupDeleteView(DeleteView):
    model = Group
    template_name = 'students/groups_confirm_delete.html'
    
    def get_success_url(self):
        return '{}?status_message={}'.format(reverse('groups'), _('Group deleted'))
