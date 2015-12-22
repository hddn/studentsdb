from django.db import models
from django.utils.translation import ugettext as _

# Create your models here.

class Exam(models.Model):

    subject = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=_(u'Title'))

    teacher = models.CharField(
        max_length=256,
        blank=True,
        verbose_name=_(u'Teacher'))

    date = models.DateTimeField(
        blank=False,
        verbose_name=_(u'Date'))

    group = models.OneToOneField('Group',
        blank=True,
        null=True,
        verbose_name=_(u'Group'),
        on_delete=models.SET_NULL)
    
    notes = models.TextField(
        blank=True,
        verbose_name=_(u'Notes'))

    def __unicode__(self):
        if self.group:
            return u'%s, %s (%s)' % (self.group, 
                                    self.subject, 
                                    self.date)
        else:
            return u'%s (%s)' % (self.group, self.date)