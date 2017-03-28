# -*- coding: utf-8 -*-
import logging

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Student


@receiver(post_save, sender=Student)
def log_student_updated_added_event(sender, **kwargs):
    """Writes info about updated or newly added student into log file"""
    logger = logging.getLogger(__name__)

    student = kwargs['instance']
    if kwargs['created']:
        logger.info("Student added: {} {} (ID: {:d})".format(student.first_name, student.last_name, student.id))
    else:
        logger.info("Student updated: {} {} (ID: {:d})".format(student.first_name, student.last_name, student.id))


@receiver(post_delete, sender=Student)
def log_student_deleted_event(sender, **kwargs):
    """Writes info about deleted student into the log file"""
    logger = logging.getLogger(__name__)

    student = kwargs['instance']
    logger.info("Student deleted: {} {} (ID: {:d})".format(student.first_name, student.last_name, student.id))
