#!/bin/sh
set -euf

do_setup() {
  wait-for-it $DATABASE_HOST:$DATABASE_PORT
  if [ "${1:-migrate}" != "no-migrate" ]; then
    # migrate may fail in concurrent startup, thus we're not
    # taking this as a failure here
    ./manage.py migrate || true
  fi
  ./manage.py collectstatic --noinput
  ./manage.py compilemessages
}

loadconfig() {
  ./manage.py camac_load
}

# Default command (from Dockerfile) is "uwsgi". This implies production mode
# and we only load config in prod mode.
if [ "$#" -lt 1 ]; then
  echo "ERROR: NO COMMAND GIVEN: $@"
  echo "Need to pass either one of these:"
  echo "   - uwsgi             to run the production server (load config), possible arguments:"
  echo "      --no-loadconfig  to skip the loadconfig step"
  echo "   - gunicorn          to run the production server (load config), possible arguments:"
  echo "      --no-loadconfig  to skip the loadconfig step"
  echo "   - hurricane         to run the production server for kubernetes (load config)"
  echo "   - hurricanedev      to run the development server for kubernetes"
  echo "   - qcluster          to run the django-q service"
  echo "   - celery            to run the celery service"
  echo "   - celerydev         to run the celery service in development mode"
  echo "   - devserver         to run the development server (takes additional args"
  echo  "    if needed)"
  echo ""
  echo "Any other command will be run as-is (for example you can run bash"
  echo "or any other mgmt command)"
  exit 1
fi

do_loadconfig="true"

case "$*" in
  *--no-loadconfig*)
    do_loadconfig="false"
    ;;
  *)
    ;;
esac

case "$1" in
  uwsgi )
    do_setup
    if [ "$do_loadconfig" = "true" ]; then
      loadconfig
    fi
    exec "$1"
    ;;
  gunicorn )
    do_setup
    if [ "$do_loadconfig" = "true" ]; then
      loadconfig
    fi
    exec gunicorn --workers "${DJANGO_GUNICORN_WORKERS:-10}" --access-logfile - --limit-request-line "${DJANGO_LIMIT_REQUEST_LINE:-8190}" --bind :"${DJANGO_SERVER_PORT:-80}" camac.wsgi
    ;;
  devserver )
    do_setup
    exec python manage.py runserver 0:80 --pythonpath /app/$APPLICATION
    ;;
  hurricane )
    exec python ./manage.py serve --static --port "${DJANGO_SERVER_PORT:-80}" --req-queue-len "${HURRICANE_REQ_QUEUE_LEN:-50}"
    ;;
  hurricanedev )
    exec python ./manage.py serve --static --autoreload --port "${DJANGO_SERVER_PORT:-80}" --req-queue-len "${HURRICANE_REQ_QUEUE_LEN:-50}"
    ;;
  qcluster )
    do_setup no-migrate
    exec python manage.py qcluster --pythonpath /app/$APPLICATION
    ;;
  qclusterdev )
    do_setup no-migrate
    watchmedo auto-restart -d . --recursive -p '*.py' -- python manage.py qcluster --pythonpath /app/$APPLICATION
    ;;
  celery )
    do_setup no-migrate
    wait-for-it redis:6379
    celery -A camac worker -l INFO -E -O fair;
    ;;
  celerydev )
    do_setup no-migrate
    wait-for-it redis:6379
    watchmedo auto-restart -d . --recursive -p '*.py' -- celery -A camac worker -l INFO -E -O fair;
    ;;
  webdav )
    do_setup no-migrate
    exec gunicorn --workers "${DJANGO_WEBDAV_GUNICORN_WORKERS:-8}" --access-logfile - --limit-request-line "${DJANGO_LIMIT_REQUEST_LINE:-8190}" --bind :"${DJANGO_WEBDAV_SERVER_PORT:-8000}" camac.wsgi_dav
    ;;
  * )
    exec "$@"
    ;;
esac
