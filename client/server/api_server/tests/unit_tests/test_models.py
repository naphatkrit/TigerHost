import pytest

from django.contrib.auth.models import User


@pytest.mark.django_db
def test_get_paas_password(username, email, password):
    user = User.objects.create_user(username, email, password)
    pass1 = user.profile.get_paas_password()
    pass2 = user.profile.get_paas_password()
    assert pass1 == pass2
