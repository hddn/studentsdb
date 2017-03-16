
from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.


class Student(models.Model):

    first_name = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=_('First Name'))

    last_name = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=_('Last Name'))

    middle_name = models.CharField(
        max_length=256,
        blank=True,
        verbose_name=_('Middle Name'),
        default='')

    birthday = models.DateField(
        blank=False,
        verbose_name=_('Birthday'),
        null=True)

    photo = models.ImageField(
        blank=True,
        verbose_name=_('Photo'),
        null=True)

    ticket = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=_('Ticket'))

    notes = models.TextField(
        blank=True,
        verbose_name=_('Notes'))

    student_group = models.ForeignKey(
        'Group',
        verbose_name=_('Group'),
        blank=False,
        null=True,
        on_delete=models.PROTECT)

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)
