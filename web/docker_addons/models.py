from __future__ import unicode_literals

import string
import uuid

from django.db import models
from django.utils import crypto


def make_container_name():
    # alphanumeric, length = 50, this gives ~290 bits of entropy
    return crypto.get_random_string(length=50, allowed_chars=string.ascii_letters + string.digits)


class ContainerInfo(models.Model):
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)

    # the name that identify this container on the docker host
    name = models.CharField(max_length=50, unique=True,
                            default=make_container_name, editable=False)

    # the ID assigned by docker host, will be set after the container is
    # actually created on docker host
    container_id = models.CharField(max_length=100, unique=True, null=True)
