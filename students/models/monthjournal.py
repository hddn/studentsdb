from django.db import models
from django.utils.translation import ugettext as _


class MonthJournal(models.Model):
    """Student Monthly Journal"""

    student = models.ForeignKey(
        'Student',
        verbose_name=_('Student'),
        blank=False,
        unique_for_month='date')

    date = models.DateField(
        verbose_name=_('Date'),
        blank=False)

    def __str__(self):
        return '{}: {:d}, {:d}'.format(self.student.last_name, self.date.month, self.date.year)


for i in range(1, 32):
    MonthJournal.add_to_class('present_day{}'.format(i), models.BooleanField(default=False))
