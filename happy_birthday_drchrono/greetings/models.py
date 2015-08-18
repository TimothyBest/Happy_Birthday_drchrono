from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

class HappyBirthday(models.Model):
    user = models.OneToOneField(User, unique=True, primary_key=True,
	                            verbose_name=_('user'), related_name='happy_birthday')
    is_active = models.BooleanField(default=False)
    sms = models.CharField(_("text"), max_length=160, null=True, blank=True)
    email_subject =  models.CharField(_("subject"), max_length=77, null=True,
	                                  blank=True)
    email_body = models.TextField(_("body"), null=True, blank=True)