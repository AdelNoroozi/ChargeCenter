#!/bin/sh
echo "--> Waiting for db to be ready"
./wait-for-it.sh db:5433

echo "Apply database migrations"
python manage.py makemigrations
python manage.py migrate
#python manage.py collectstatic --clear --noinput
#python manage.py collectstatic --noinput

echo "--> Starting web process"
gunicorn config.wsgi:application --workers=5 --threads=2 -b 0.0.0.0:8000