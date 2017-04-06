from django.utils.translation import ugettext as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from crispy_forms.bootstrap import FormActions
from registration.forms import RegistrationForm


class RegisterForm(RegistrationForm):

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'
        self.helper.help_text_inline = True
        self.helper.html5_required = False

        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'

        self.helper.layout = Layout(
                'username',
                'email',
                'password1',
                'password2',
                FormActions(
                    Submit('register', _('Register'), css_class='btn btn-primary'),
                ))
