#!/bin/sh
set -euf

loadconfig() {
  wait-for-it "$DATABASE_HOST:$DATABASE_PORT" -- ./manage.py camac_load
}

migrate() {
  wait-for-it "$DATABASE_HOST:$DATABASE_PORT" -- ./manage.py migrate
}

# Default command (from Dockerfile) is "uwsgi". This implies production mode
# and we only load config in prod mode.
if [ "$#" -lt 1 ]; then
  echo "ERROR: NO COMMAND GIVEN: $*"
  echo "Need to pass either one of these:"
  echo "   - devserver         to run the development server"
  echo "   - uwsgi             to run the production server (load config), possible arguments:"
  echo "      --no-loadconfig  to skip the loadconfig step"
  echo "   - gunicorn          to run the production server without integrated webdav (load"
  echo "                       config), possible arguments:"
  echo "      --no-loadconfig  to skip the loadconfig step"
  echo "   - gunicorn_k8s      to run the production server without integrated webdav and"
  echo "                       without any implicit setup (loadconfig, migrate)"
  echo "   - hurricane         to run the production server for kubernetes"
  echo "   - hurricanedev      to run the development server mimicking kubernetes env"
  echo "   - qcluster          to run the django-q service"
  echo "   - celery            to run the celery service"
  echo "   - celerydev         to run the celery service in development mode"
  echo "   - webdav            to run the webdav server via gunicorn and webdav.wsgi"
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
  devserver )
    migrate
    exec python manage.py runserver 0:80 --pythonpath /app/$APPLICATION
    ;;
  uwsgi )
    migrate
    if [ "$do_loadconfig" = "true" ]; then
      loadconfig
    fi
    exec "$1"
    ;;
  gunicorn )
    migrate
    if [ "$do_loadconfig" = "true" ]; then
      loadconfig
    fi
    exec gunicorn --workers "${DJANGO_GUNICORN_WORKERS:-10}" --access-logfile - --limit-request-line "${DJANGO_LIMIT_REQUEST_LINE:-8190}" --bind :"${DJANGO_SERVER_PORT:-80}" camac.wsgi_gunicorn
    ;;
  gunicorn_k8s )
    # K8s mode: All setup (loadconfig, migrate) must be done explicitly
    # in an init task or similar
    exec gunicorn --workers "${DJANGO_GUNICORN_WORKERS:-10}" --access-logfile - --limit-request-line "${DJANGO_LIMIT_REQUEST_LINE:-8190}" --bind :"${DJANGO_SERVER_PORT:-80}" camac.wsgi_gunicorn
    ;;
  hurricane )
    exec python ./manage.py serve --static --port "${DJANGO_SERVER_PORT:-80}" --req-queue-len "${HURRICANE_REQ_QUEUE_LEN:-150}" --workers "${HURRICANE_WORKERS:-4}"
    ;;
  hurricanedev )
    migrate
    exec python ./manage.py serve --static --autoreload --port "${DJANGO_SERVER_PORT:-80}" --req-queue-len "${HURRICANE_REQ_QUEUE_LEN:-50}"
    ;;
  qcluster )
    exec python manage.py qcluster --pythonpath /app/$APPLICATION
    ;;
  qclusterdev )
    watchmedo auto-restart -d . --recursive -p '*.py' -- python manage.py qcluster --pythonpath /app/$APPLICATION
    ;;
  celery )
    wait-for-it ${REDIS_HOST:-redis}:${REDIS_PORT:-6379}
    celery -A camac worker -l INFO -E -O fair;
    ;;
  celerydev )
    wait-for-it ${REDIS_HOST:-redis}:${REDIS_PORT:-6379}
    watchmedo auto-restart -d . --recursive -p '*.py' -- celery -A camac worker -l INFO -E -O fair;
    ;;
  webdav )
    exec gunicorn --workers "${DJANGO_WEBDAV_GUNICORN_WORKERS:-8}" --access-logfile - --limit-request-line "${DJANGO_LIMIT_REQUEST_LINE:-8190}" --bind :"${DJANGO_WEBDAV_SERVER_PORT:-8000}" camac.wsgi_dav
    ;;
  migrate_and_loadconfig )
    migrate
    loadconfig
    ;;
  * )
    exec "$@"
    ;;
esac
