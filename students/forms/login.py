from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from crispy_forms.bootstrap import FormActions


class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        self.helper.help_text_inline = True
        self.helper.html5_required = False

        self.helper.label_class = 'col-xs-2 control-label'
        self.helper.field_class = 'col-xs-10'

        self.helper.layout = Layout(
            self.helper.layout, FormActions(
                Submit('login_button', _(u'Login'), css_class="btn btn-primary"),
            ))

    class Meta:
        model = User
        fields = ['username', 'password']
