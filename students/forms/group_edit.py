# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.forms import ModelForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from crispy_forms.bootstrap import FormActions

from ..models import Group


class GroupEditForm(ModelForm):
    
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

    class Meta:
        model = Group
        fields = ['title', 'leader', 'notes']