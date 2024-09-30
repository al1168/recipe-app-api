#!/bin/sh

set -e
echo "Printing all environment variables:"
env
echo 'ALLOWED_HOSTS:' $ALLOWED_HOSTS
python manage.py wait_for_db
python manage.py collectstatic --noinput
python manage.py migrate

uwsgi --socket :9000 --workers 4 --master --enable-threads --module app.wsgi --buffer-size=32768