#!/bin/sh

wait-for-it "$DATABASE_HOST:$DATABASE_PORT" -- ./manage.py migrate

# All parameters to the script are appended as arguments to `manage.py serve`

set -x

./manage.py collectstatic --noinput

set -e

# ./manage.py camac_load

./manage.py serve --static --port "${DJANGO_SERVER_PORT:-80}" --req-queue-len "${HURRICANE_REQ_QUEUE_LEN:-50}" "$@"
