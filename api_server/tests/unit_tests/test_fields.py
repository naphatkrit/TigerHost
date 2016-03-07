import pytest

from enum import Enum

from api_server.addons.state import AddonState
from api_server.fields import EnumField
from api_server.models import Addon


class SampleEnum(Enum):
    value1 = 1
    value2 = 2
    value3 = 3


def test_enum_field_deconstruct():
    field = EnumField(SampleEnum)
    _, _, args, kwargs = field.deconstruct()
    new_field = EnumField(*args, **kwargs)
    assert field.enum_class == new_field.enum_class


@pytest.mark.django_db
def test_sample_model_simple(make_app):
    obj = Addon.objects.create(
        provider_name='test', app=make_app, state=AddonState.waiting_for_provision)
    assert obj.state == AddonState.waiting_for_provision
    obj.state = AddonState.deprovisioned
    obj.save()


@pytest.mark.django_db
def test_sample_model_type(make_app):
    obj = Addon.objects.create(
        provider_name='test', app=make_app, state=AddonState.waiting_for_provision)
    obj.state = SampleEnum.value1
    with pytest.raises(ValueError):
        obj.save()


@pytest.mark.django_db
def test_sample_model_query(make_app):
    Addon.objects.create(
        provider_name='test', app=make_app, state=AddonState.waiting_for_provision)
    Addon.objects.create(
        provider_name='test', app=make_app, state=AddonState.waiting_for_provision)
    Addon.objects.create(provider_name='test', app=make_app,
                         state=AddonState.provisioned)
    assert Addon.objects.filter(
        state=AddonState.waiting_for_provision).count() == 2
    assert Addon.objects.filter(state=AddonState.provisioned).count() == 1

    assert Addon.objects.filter(
        state__in=[AddonState.waiting_for_provision, AddonState.provisioned]).count() == 3
    assert Addon.objects.filter(
        state__in=[AddonState.waiting_for_provision, AddonState.deprovisioned]).count() == 2
    assert Addon.objects.filter(
        state__in=[AddonState.waiting_for_provision, AddonState.deprovisioned]).count() == 2
