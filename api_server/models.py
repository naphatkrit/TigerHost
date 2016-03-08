from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.models import User
from django.core.signing import Signer
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.db import models
from django.utils import crypto
from jsonfield import JSONField

from api_server.addons.state import AddonState
from api_server.fields import EnumField


def make_secret():
    return crypto.get_random_string(length=50)


class PaasCredential(models.Model):
    profile = models.ForeignKey(
        'Profile', on_delete=models.CASCADE, related_name='paas_credential_set')
    backend = models.CharField(max_length=50)
    password_seed = models.CharField(default=make_secret, max_length=50)

    def get_password(self):
        signer = Signer()
        return signer.sign(self.password_seed)

    class Meta:
        unique_together = ('profile', 'backend')


class Profile(models.Model):

    class NoCredentials(Exception):
        pass

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def get_paas_backends(self):
        """Return the list of names of backends that this user has
        a credential for.

        @rtype: list
            backend names (str)
        """
        backends = [x.backend for x in self.paas_credential_set.all()]
        if settings.DEFAULT_PAAS_BACKEND not in backends:
            PaasCredential.objects.create(
                profile=self, backend=settings.DEFAULT_PAAS_BACKEND)
            backends.append(settings.DEFAULT_PAAS_BACKEND)
        return backends

    def get_credential(self, backend):
        """Get the credential for this backend.

        @type backend: str

        @rtype: PaasCredential

        @raises e: Profile.NoCredentials
        """
        for x in self.paas_credential_set.all():
            if x.backend == backend:
                return x
        raise Profile.NoCredentials


class App(models.Model):

    # don't call this id to avoid conflicting with
    # Django's generated primary key
    # NOTE: unique implies index
    app_id = models.CharField(max_length=128, unique=True, validators=[
                              RegexValidator(regex=r'^[a-z0-9-]+$')])
    backend = models.CharField(max_length=50)

    @classmethod
    def get_backend(cls, app_id):
        """Given an app ID, return the backend name.

        @rtype: str
        @raises e: App.DoesNotExist
        """
        return cls.objects.get(app_id=app_id).backend

    def save(self, *args, **kwargs):
        # call the validation methods
        self.full_clean()
        super(App, self).save(*args, **kwargs)


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


def make_default_credential(sender, instance, created, **kwargs):
    try:
        if created:
            credential, created = PaasCredential.objects.get_or_create(
                profile=instance, backend=settings.DEFAULT_PAAS_BACKEND)
            if created:
                try:
                    credential.save()
                except Exception:
                    if settings.DEBUG:
                        raise
    except Exception:
        if settings.DEBUG:
            raise

post_save.connect(make_default_credential, sender=Profile)


class Addon(models.Model):
    provider_name = models.CharField(max_length=50)
    provider_uuid = models.UUIDField()
    # TODO on app deletion, should deprovision all resources
    app = models.ForeignKey(App, on_delete=models.SET_NULL, null=True)
    state = EnumField(AddonState)
    config = JSONField(null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
