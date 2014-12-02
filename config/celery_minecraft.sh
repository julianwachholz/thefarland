#!/bin/bash

ROOT=/data/http/django
source $ROOT/.env/bin/activate

export NEW_RELIC_CONFIG_FILE=/data/http/django/thefarland/config/newrelic.ini
export NEW_RELIC_APP_NAME="thefar.land (Celery);thefar.land"
exec newrelic-admin run-program celery -A thefarland worker --loglevel=INFO -Q 'default,minecraft'
