#!/usr/bin/env bash

sleep 2
while ! nc -z $SQL_HOST $SQL_PORT; do
  sleep 1
done

echo "check migrations"
if ! ./manage.py makemigrations --check # --dry-run
then
    echo "Need to make migrations"
    exit 1
fi

if [[ "$CI" -eq "1" ]];
then
    coverage run ./manage.py test --keepdb
    coverage report
    coveralls
    flake8
    exit 0
fi

./manage.py flush --no-input
./manage.py migrate
./manage.py collectstatic --no-input

gunicorn ocular_back.wsgi:application --bind 0.0.0.0:8000 --reload
