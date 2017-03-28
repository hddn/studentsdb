
import logging

from django import forms
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _
from django.views.generic.edit import FormView

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from studentsdb.settings import ADMIN_EMAIL


class ContactForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('contact_admin')

        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'

        self.helper.add_input(Submit('send_button', _('Send')))

    from_email = forms.EmailField(
        label=_('Your E-mail'))

    subject = forms.CharField(
        label=_('Subject'),
        max_length=128)

    message = forms.CharField(
        label=_('Message'),
        max_length=2560,
        widget=forms.Textarea)


class ContactView(FormView):
    template_name = 'contact_admin/form.html'
    form_class = ContactForm

    def form_valid(self, form):
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']
        from_email = form.cleaned_data['from_email']

        try:
            send_mail(subject, message, from_email, [ADMIN_EMAIL])

        except Exception:
            message = _('An error occurred')
            logger = logging.getLogger(__name__)
            logger.exception(message)
        else:
            message = _('Message send successfully')

        return HttpResponseRedirect('{}?status_message={}'.format(reverse('contact_admin'), message))
