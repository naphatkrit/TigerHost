#!/usr/bin/env bash

set -e

python manage.py migrate
gunicorn api_server.wsgi:application -w 2 -b :8000 --reload
