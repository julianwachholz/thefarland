#!/bin/bash

ROOT=/data/http/django
source $ROOT/.env/bin/activate

export NEW_RELIC_CONFIG_FILE=/data/http/django/thefarland/config/newrelic.ini
export NEW_RELIC_APP_NAME="thefar.land (Django);thefar.land"
exec newrelic-admin run-program uwsgi --ini /data/http/django/thefarland/config/uwsgi.ini
