#!/usr/bin/env bash

set -e

# using 0.0.0.0 means to not care what IP it is actually at
python manage.py runserver 0.0.0.0:8000
