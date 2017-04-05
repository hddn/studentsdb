from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.


class Group(models.Model):

    title = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=_('Title'))

    leader = models.OneToOneField(
        'Student',
        blank=True,
        null=True,
        verbose_name=_('Leader'),
        on_delete=models.SET_NULL)
    
    notes = models.TextField(
        blank=True,
        verbose_name=_('Notes'))

    def __str__(self):
        if self.leader:
            return '{} ({} {})'.format(self.title, self.leader.first_name, self.leader.last_name)
        else:
            return '{}'.format(self.title)
