#!/bin/sh
set -euf

loadconfig() {
  wait-for-it "$DATABASE_HOST:$DATABASE_PORT" -- ./manage.py camac_load
}

clear_cache() {
  # to be run *after* loadconfig
  wait-for-it "$DJANGO_CACHE_LOCATION" -- ./manage.py clear_cache
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
  echo "   - qcluster          to run the django-q service"
  echo "   - celery            to run the celery service"
  echo "   - celerydev         to run the celery service in development mode"
  echo "   - celery-beat       to run the celery beat scheduler"
  echo "   - celery-beat-dev   to run the celery beat scheduler in development mode"
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
    exec gunicorn --workers "${DJANGO_GUNICORN_WORKERS:-10}" --threads "${DJANGO_GUNICORN_THREADS:-1}" --access-logfile - --limit-request-line "${DJANGO_LIMIT_REQUEST_LINE:-8190}" --bind :"${DJANGO_SERVER_PORT:-80}" camac.wsgi_gunicorn
    ;;
  gunicorn_k8s )
    # K8s mode: All setup (loadconfig, migrate) must be done explicitly
    # in an init task or similar
    exec gunicorn --workers "${DJANGO_GUNICORN_WORKERS:-10}" --threads "${DJANGO_GUNICORN_THREADS:-1}" --timeout "${DJANGO_GUNICORN_TIMEOUT:-90}" --access-logfile - --limit-request-line "${DJANGO_LIMIT_REQUEST_LINE:-8190}" --bind :"${DJANGO_SERVER_PORT:-80}" --max-requests "${DJANGO_GUNICORN_MAX_REQUESTS:-0}" --max-requests-jitter "${DJANGO_GUNICORN_MAX_REQUESTS_JITTER:-0}" camac.wsgi_gunicorn
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
  celery-beat)
    exec celery -A camac beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
      ;;
  celery-beat-dev)
    exec watchmedo auto-restart -d . --recursive -p '*.py' -- celery -A camac beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
  ;;
  webdav )
    exec gunicorn --workers "${DJANGO_WEBDAV_GUNICORN_WORKERS:-8}" --threads "${DJANGO_WEBDAV_GUNICORN_THREADS:-1}" --access-logfile - --limit-request-line "${DJANGO_LIMIT_REQUEST_LINE:-8190}" --bind :"${DJANGO_WEBDAV_SERVER_PORT:-8000}" --max-requests "${DJANGO_WEBDAV_MAX_REQUESTS:-0}" --max-requests-jitter "${DJANGO_WEBDAV_MAX_REQUESTS_JITTER:-0}" camac.wsgi_dav
    ;;
  migrate_and_loadconfig )
    migrate
    loadconfig
    clear_cache
    ;;
  * )
    exec "$@"
    ;;
esac
