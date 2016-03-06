import pytest

from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

from api_server.models import App, PaasCredential, Profile


@pytest.mark.django_db
def test_profile_get_paas_backends(user, settings):
    profile = user.profile
    assert profile.get_paas_backends() == [settings.DEFAULT_PAAS_BACKEND]

    PaasCredential.objects.create(profile=profile, backend='backend1')
    assert set(profile.get_paas_backends()) == {
        settings.DEFAULT_PAAS_BACKEND, 'backend1'}

    c = PaasCredential.objects.get(profile=profile, backend=settings.DEFAULT_PAAS_BACKEND)
    c.delete()
    assert profile.paas_credential_set.count() == 1
    assert set(profile.get_paas_backends()) == {
        settings.DEFAULT_PAAS_BACKEND, 'backend1'}
    assert profile.paas_credential_set.count() == 2


@pytest.mark.django_db
def test_profile_get_credential(user, settings):
    profile = user.profile
    PaasCredential.objects.create(profile=profile, backend='backend1')
    c = profile.get_credential(settings.DEFAULT_PAAS_BACKEND)
    assert c.backend == settings.DEFAULT_PAAS_BACKEND

    with pytest.raises(Profile.NoCredentials):
        profile.get_credential('doesnotexist')


@pytest.mark.django_db
def test_credentials_get_password(user):
    profile = user.profile
    c = PaasCredential.objects.create(
        profile=profile, backend='backend1')
    pass1 = c.get_password()
    pass2 = c.get_password()
    assert pass1 == pass2


@pytest.mark.django_db
def test_credentials_profile_unique(user):
    profile = user.profile
    PaasCredential.objects.create(profile=profile, backend='backend1')
    PaasCredential.objects.create(profile=profile, backend='backend2')
    with pytest.raises(IntegrityError):
        PaasCredential.objects.create(
            profile=profile, backend='backend1')


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
        App.objects.create(app_id=name, backend='testing')


@pytest.mark.django_db
def test_app_get_backend():
    with pytest.raises(App.DoesNotExist):
        App.get_backend('doesnotexit')

    App.objects.create(app_id='dummy1', backend='backend1')
    assert App.get_backend('dummy1') == 'backend1'
