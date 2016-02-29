import pytest

from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

from api_server.models import App, PaasCredential, Profile


@pytest.mark.django_db
def test_profile_get_providers(user, settings):
    profile = user.profile
    assert profile.get_providers() == [settings.DEFAULT_PAAS_PROVIDER]

    PaasCredential.objects.create(profile=profile, provider_name='provider1')
    assert set(profile.get_providers()) == {
        settings.DEFAULT_PAAS_PROVIDER, 'provider1'}


@pytest.mark.django_db
def test_profile_get_credential(user, settings):
    profile = user.profile
    PaasCredential.objects.create(profile=profile, provider_name='provider1')
    c = profile.get_credential(settings.DEFAULT_PAAS_PROVIDER)
    assert c.provider_name == settings.DEFAULT_PAAS_PROVIDER

    with pytest.raises(Profile.NoCredentials):
        profile.get_credential('doesnotexist')


@pytest.mark.django_db
def test_credentials_get_password(user):
    profile = user.profile
    c = PaasCredential.objects.create(
        profile=profile, provider_name='provider1')
    pass1 = c.get_password()
    pass2 = c.get_password()
    assert pass1 == pass2


@pytest.mark.django_db
def test_credentials_profile_unique(user):
    profile = user.profile
    PaasCredential.objects.create(profile=profile, provider_name='provider1')
    PaasCredential.objects.create(profile=profile, provider_name='provider2')
    with pytest.raises(IntegrityError):
        PaasCredential.objects.create(
            profile=profile, provider_name='provider1')


@pytest.mark.django_db
@pytest.mark.parametrize('name', [
    'Caps',
    'underscore_testing',
    '!@#$%^',
    '////',
    '',
])
def test_app_id_validation(name):
    with pytest.raises(ValidationError):
        App.objects.create(app_id=name, provider_name='testing')


@pytest.mark.django_db
def test_app_get_provider_name():
    with pytest.raises(App.DoesNotExist):
        App.get_provider_name('doesnotexit')

    App.objects.create(app_id='dummy1', provider_name='provider1')
    assert App.get_provider_name('dummy1') == 'provider1'
