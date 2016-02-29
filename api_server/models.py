from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.models import User
from django.core.signing import Signer
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.db import models
from django.utils import crypto


def make_secret():
    return crypto.get_random_string(length=50)


class Profile(models.Model):

    class NoCredentials(Exception):
        pass

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def get_providers(self):
        """Return the list of names of providers that this user has
        a credential for.

        @rtype: list
            provider names (str)
        """
        return [x.provider_name for x in self.paas_credential_set.all()]

    def get_credential(self, provider_name):
        """Get the credential for this provider.

        @type provider_name: str

        @rtype: PaasCredential

        @raises e: Profile.NoCredentials
        """
        for x in self.paas_credential_set.all():
            if x.provider_name == provider_name:
                return x
        raise Profile.NoCredentials


class PaasCredential(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='paas_credential_set')
    provider_name = models.CharField(max_length=50)
    password_seed = models.CharField(default=make_secret, max_length=50)

    def get_password(self):
        signer = Signer()
        return signer.sign(self.password_seed)

    class Meta:
        unique_together = ('profile', 'provider_name')


class App(models.Model):

    # don't call this id to avoid conflicting with
    # Django's generated primary key
    # NOTE: unique implies index
    app_id = models.CharField(max_length=128, unique=True, validators=[
                              RegexValidator(regex=r'^[a-z0-9-]+$')])
    provider_name = models.CharField(max_length=50)

    @classmethod
    def get_provider_name(cls, app_id):
        """Given an app ID, return the provider name.

        @rtype: str
        @raises e: App.DoesNotExist
        """
        return cls.objects.get(app_id=app_id).provider_name

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
                profile=instance, provider_name=settings.DEFAULT_PAAS_PROVIDER)
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
