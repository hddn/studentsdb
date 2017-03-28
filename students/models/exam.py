from django.db import models
from django.utils.translation import ugettext as _

# Create your models here.


class Exam(models.Model):

    subject = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=_('Title'))

    teacher = models.CharField(
        max_length=256,
        blank=True,
        verbose_name=_('Teacher'))

    date = models.DateTimeField(
        blank=False,
        verbose_name=_('Date'))

    group = models.OneToOneField(
        'Group',
        blank=True,
        null=True,
        verbose_name=_('Group'),
        on_delete=models.SET_NULL)
    
    notes = models.TextField(
        blank=True,
        verbose_name=_('Notes'))

    def __str__(self):
        if self.group:
            return '{}, {} ({})'.format(self.group.title, self.subject, self.date)
        else:
            return '{} ({})'.format(self.subject, self.date)
