from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.models import User
from django.core.signing import Signer
from django.db.models.signals import post_save
from django.db import models
from django.utils import crypto


def make_secret():
    return crypto.get_random_string(length=50)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    paas_password_seed = models.CharField(default=make_secret, max_length=50)

    def get_paas_password(self):
        signer = Signer()
        return signer.sign(self.paas_password_seed)


def make_new_profile(sender, instance, created, **kwargs):
    # see http://stackoverflow.com/a/965883/130164
    # Use a try because the first user (super user) is created before other tables are created.
    # That is, this fails during syncdb upon initial database setup, because
    # it creates a superuser before User_Profile table is added (we add that
    # by running migrations after).
    try:
        if created:
            profile, created = Profile.objects.get_or_create(
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

post_save.connect(make_new_profile, sender=User)
