#!/usr/bin/env bash

set -e

celery -A api_server worker -l info
