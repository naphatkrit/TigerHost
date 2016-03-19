from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.db import models
from enum import Enum


class EnumField(models.IntegerField):
    desciption = 'A field of enum values'

    def __init__(self, enum_class, *args, **kwargs):
        assert issubclass(enum_class, Enum)
        self.enum_class = enum_class
        super(self.__class__, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(self.__class__, self).deconstruct()
        kwargs['enum_class'] = self.enum_class
        return name, path, args, kwargs

    def to_python(self, value):
        """return either None or self.enum_class instance"""
        if isinstance(value, self.enum_class):
            return value
        value = super(self.__class__, self).to_python(value)
        if isinstance(value, int):
            return self.enum_class(value)
        assert value is None
        return None

    def from_db_value(self, value, expression, connection, context):
        """return either None or self.enum_class instance"""
        # can't call super. See
        # https://docs.djangoproject.com/en/1.9/ref/models/fields/#django.db.models.Field.from_db_value
        if isinstance(value, int):
            try:
                return self.enum_class(value)
            except ValueError:
                raise ValidationError(
                    'Invalid enum integer value {} for {}'.format(value, self.enum_class))

        assert value is None
        return None

    def get_prep_value(self, value):
        """return either None or the result of calling super class's method"""
        if value is None:
            return value
        if isinstance(value, self.enum_class):
            return super(self.__class__, self).get_prep_value(value.value)
        if isinstance(value, Enum):
            raise ValueError('{} is of the wrong Enum type.'.format(value))
        return super(self.__class__, self).get_prep_value(value)

    def get_prep_lookup(self, lookup_type, value):
        """process the parameter and call through to the superclass"""
        if value is None:
            return super(self.__class__, self).get_prep_lookup(lookup_type, value)
        if lookup_type == 'in':
            value = [v.value for v in value]
            return super(self.__class__, self).get_prep_lookup(lookup_type, value)
        if lookup_type == 'exact':
            return super(self.__class__, self).get_prep_lookup(lookup_type, value.value)
        raise TypeError('Lookup type {} is not supported.'.format(lookup_type))

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        if not isinstance(value, self.enum_class):
            raise ValueError('{} is not of type {}'.format(
                value, self.enum_class))
        return super(self.__class__, self).value_to_string(value.value)
