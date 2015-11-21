from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _


class UserProfile(models.Model):
    """Keeps user extra data"""

    user = models.OneToOneField(User)

    class Meta(object):
        verbose_name = _(u'User Profile')

    mobile_phone = models.CharField(
        max_length=12,
        blank=True,
        verbose_name=(u'Mobile Phone'),
        default='')

    def __unicode__(self):
        return self.user.username