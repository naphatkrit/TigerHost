from __future__ import unicode_literals

import string
import uuid

from django.db import models
from django.utils import crypto


def make_instance_identifier():
    # alphanumeric, start with a letter, max length 63
    return crypto.get_random_string(length=1, allowed_chars=string.ascii_lowercase) + crypto.get_random_string(length=62, allowed_chars=string.ascii_lowercase + string.digits)


def make_db_name():
    # alphanumeric, start with a letter, max length 63
    return crypto.get_random_string(length=1, allowed_chars=string.ascii_lowercase) + crypto.get_random_string(length=62, allowed_chars=string.ascii_lowercase + string.digits)


def make_username():
    # alphanumeric, begin with a letter, max length 16
    return crypto.get_random_string(length=1, allowed_chars=string.ascii_lowercase) + crypto.get_random_string(length=15, allowed_chars=string.ascii_lowercase + string.digits)


def make_password():
    # printable, max length 30, cannot contain /, ", @
    allowed_chars = string.ascii_letters + string.digits + string.punctuation
    allowed_chars = allowed_chars.replace(
        '/', '').replace('"', '').replace('@', '')
    return crypto.get_random_string(length=30, allowed_chars=allowed_chars)


class DbInstance(models.Model):
    # NOTE: using editable=False means to skip validation and to not display
    # in admin page. It does NOT mean the field is immutable.
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    aws_instance_identifier = models.CharField(
        max_length=63, unique=True, default=make_instance_identifier, editable=False)
    db_name = models.CharField(
        max_length=64, default=make_db_name, editable=False)
    master_username = models.CharField(
        max_length=16, default=make_username, editable=False)
    master_password = models.CharField(
        max_length=30, default=make_password, editable=False)
