#!/bin/bash

source /data/http/django/.env/bin/activate
uwsgi --ini /data/http/django/thefarland/config/uwsgi.ini

deactivate
