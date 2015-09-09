# -*- coding: utf-8 -*-

from django.db import models

# Create your models here.

class Exam(models.Model):

    subject = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=u'Назва')

    teacher = models.CharField(
        max_length=256,
        blank=True,
        verbose_name=u'Викладач')

    date = models.DateTimeField(
        blank=False,
        verbose_name=u'Дата')

    group = models.OneToOneField('Group',
        blank=True,
        null=True,
        verbose_name=u'Група',
        on_delete=models.SET_NULL)
    
    notes = models.TextField(
        blank=True,
        verbose_name=u'Додаткові нотатки')

    def __unicode__(self):
        if self.group:
            return u'%s, %s (%s)' % (self.group, 
                                    self.subject, 
                                    self.date)
        else:
            return u'%s (%s)' % (self.group, self.date)