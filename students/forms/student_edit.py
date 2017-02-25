from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.forms import ModelForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from crispy_forms.bootstrap import FormActions

from ..models import Student


class StudentEditForm(ModelForm):

    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'middle_name',
                  'birthday', 'photo', 'ticket',
                  'student_group', 'notes']

    def __init__(self, *args, **kwargs):
        super(StudentEditForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        if kwargs['instance'] is not None:
            add_form = False
        else:
            add_form = True

        if add_form:
            self.helper.form_action = reverse('students_add')
        else:
            self.helper.form_action = reverse('students_edit', kwargs={'pk': kwargs['instance'].id})

        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        self.helper.help_text_inline = True
        self.helper.html5_required = False
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'

        self.helper.layout = Layout(
            self.helper.layout, FormActions(
                Submit('add_button', _(u'Save'), css_class="btn btn-primary"),
                Submit('cancel_button', _(u'Cancel'), css_class="btn btn-link"),
            ))
