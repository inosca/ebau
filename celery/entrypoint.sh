#!/bin/sh

wait-for-it db:5432 -- wait-for-it redis:6379;

if [ "$ENV" = "dev" ]; then
    watchmedo auto-restart -d . --recursive -p '*.py' -- celery -A camca worker -l INFO -E -O fair;
else
    celery -A camac worker -l INFO -E -O fair;
fi
