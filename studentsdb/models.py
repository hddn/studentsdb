from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _


class UserProfile(models.Model):
    """Keep user extra data"""

    user = models.OneToOneField(User)

    class Meta(object):
        verbose_name = _('User Profile')

    mobile_phone = models.CharField(
        max_length=12,
        blank=True,
        verbose_name=_('Mobile Phone'),
        default='')

    def __str__(self):
        return self.user.username
