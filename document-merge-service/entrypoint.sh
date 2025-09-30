#!/bin/bash

# DMS entrypoint.
#
#
if [ "$#" -lt 1 ]; then
  echo "ERROR: NO COMMAND GIVEN: $*"
  echo "Need to pass either one of these:"
  echo " - init_db   - initializes DB, loads data (unless disabled via env"
  echo "               var), exits. Useful for K8s environments"
  echo " - devserver - migrate DB (but no loaddata), then starts dev server"
  echo " - gunicorn  - initializes db, loads data (unless disabled"
  echo "               via env var), runs gunicorn"
  echo ""
  echo "Any other command will be run as-is (for example you can run bash"
  echo "or any other mgmt command)"
  exit 1
fi

set -e

migrate() {
  if [ "$MIGRATE_ON_STARTUP" = 'true' ]; then
    echo "Applying DB changes if needed"
    python ./manage.py migrate
  fi
}

load_data() {
  if [ "$LOAD_TEMPLATES_ON_STARTUP" = 'true' ]; then
    echo "Loading templates"
    python manage.py loaddata /tmp/document-merge-service/dump.json
    python manage.py upload_local_templates -s '/tmp/document-merge-service/templatefiles/*.docx'
    python manage.py upload_local_templates -s '/tmp/document-merge-service/templatefiles/*.xlsx'
  fi
}

GUNICORN_CONFIG=${GUNICORN_CONFIG:-/app/document_merge_service/gunicorn.py}

command="$1"
echo "DMS startup: $command"

wait-for-it "$DATABASE_HOST:${DATABASE_PORT:-5432}"

case "$command" in
  init_db )
    migrate
    load_data
    exit 0
    ;;
  devserver )
    migrate
    exec python manage.py runserver 0.0.0.0:8000
    ;;
  gunicorn )
    migrate
    load_data
    exec gunicorn -c "$GUNICORN_CONFIG"
    ;;
  * )
    exec "$@"
    ;;
esac
