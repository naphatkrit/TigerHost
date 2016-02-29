import pytest

from django.contrib.auth.models import User
from django.db.utils import IntegrityError

from api_server.models import PaasCredential


@pytest.fixture(scope='function')
def user(username, email, password):
    user = User.objects.create_user(username, email, password)
    return user


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
