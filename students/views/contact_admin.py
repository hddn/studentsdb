
import logging

from django.shortcuts import render
from django import forms
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from django.views.generic.edit import FormView

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

        self.helper.add_input(Submit('send_button', _(u'Send'))) 

    from_email = forms.EmailField(
        label=_(u'Your E-mail'))

    subject = forms.CharField(
        label=_(u'Subject'),
        max_length=128)

    message = forms.CharField(
        label=_(u'Message'),
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
            message = _(u'An error occurred')
            logger = logging.getLogger(__name__)
            logger.exception(message)
        else:
            message = _(u'Message send successfully')

        return HttpResponseRedirect(
            u'%s?status_message=%s' % (reverse('contact_admin'), message))
