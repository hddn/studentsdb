from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.translation import ugettext as _
from django.views.generic import ListView, UpdateView, DeleteView, CreateView

from braces.views import FormValidMessageMixin

from ..models import Group
from ..forms import GroupEditForm
from ..util import get_current_group

GROUPS_NUM = 3  # number of groups for pagination


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


class GroupUpdateView(FormValidMessageMixin, UpdateView):
    model = Group
    template_name = 'students/groups_edit.html'
    form_class = GroupEditForm
    success_url = reverse_lazy('groups')
    form_valid_message = _('Group update successful!')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(reverse('groups'))
        else:
            return super(GroupUpdateView, self).post(request, *args, **kwargs)


class GroupAddView(FormValidMessageMixin, CreateView):
    model = Group
    template_name = 'students/groups_add.html'
    form_class = GroupEditForm
    success_url = reverse_lazy('groups')
    form_valid_message = _('New group was added')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(reverse('groups'))
        else:
            return super(GroupAddView, self).post(request, *args, **kwargs)


class GroupDeleteView(FormValidMessageMixin, DeleteView):
    model = Group
    template_name = 'students/groups_confirm_delete.html'
    success_url = reverse_lazy('groups')

    def get_form_valid_message(self):
        return 'Group {} deleted!'.format(self.object.title)
