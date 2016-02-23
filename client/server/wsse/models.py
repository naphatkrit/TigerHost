from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

from wsse.utils import make_secret


class WsseProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    secret = models.CharField(default=make_secret, max_length=50)


def make_new_wsse_profile(sender, instance, created, **kwargs):
    # see http://stackoverflow.com/a/965883/130164
    # Use a try because the first user (super user) is created before other tables are created.
    # That is, this fails during syncdb upon initial database setup, because
    # it creates a superuser before User_Profile table is added (we add that
    # by running migrations after).
    try:
        if created:
            profile, created = WsseProfile.objects.get_or_create(
                user=instance)
            if created:
                try:
                    profile.save()
                except Exception, e:
                    if settings.DEBUG:
                        raise e
    except Exception, e:
        if settings.DEBUG:
            raise e

post_save.connect(make_new_wsse_profile, sender=User)
