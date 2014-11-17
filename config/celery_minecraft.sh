#!/bin/bash

ROOT=/data/http/django
source $ROOT/.env/bin/activate
celery -A thefarland worker --loglevel=INFO -Q 'default,minecraft'

deactivate
