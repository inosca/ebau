#!/bin/sh
set -euf

loadconfig() {
  wait-for-it "$DATABASE_HOST:$DATABASE_PORT" -- ./manage.py camac_load
}

clear_cache() {
  # to be run *after* loadconfig
  # if cache is set to redis, the backend wants an URL redis://, but wait-for-it
  # cannot deal with that. it needs plain host:port syntax.
  case "${DJANGO_USE_REDIS_CACHE:-false}" in
    true)
      cache_location="${REDIS_HOST:-redis}:${REDIS_PORT:-6379}"
      ;;
    *)
      cache_location="${DJANGO_CACHE_LOCATION#*://}"
      ;;
  esac

  # If the cache is not available, we treat this as a "recoverable" issue and
  # continue anyway, thus the "|| true"
  wait-for-it "$cache_location" -- ./manage.py clear_cache || true
}

migrate() {
  wait-for-it "$DATABASE_HOST:$DATABASE_PORT" -- ./manage.py migrate
}

run_gunicorn() {
  exec gunicorn \
    --workers "${DJANGO_GUNICORN_WORKERS:-10}" \
    --threads "${DJANGO_GUNICORN_THREADS:-1}" \
    --timeout "${DJANGO_GUNICORN_TIMEOUT:-90}" \
    --access-logfile - \
    --limit-request-line "${DJANGO_LIMIT_REQUEST_LINE:-8190}" \
    --bind :"${DJANGO_SERVER_PORT:-80}" \
    --max-requests "${DJANGO_GUNICORN_MAX_REQUESTS:-0}" \
    --max-requests-jitter "${DJANGO_GUNICORN_MAX_REQUESTS_JITTER:-0}" \
    camac.wsgi_gunicorn
}

run_celery() {
  # Arguments (any combination):
  #   --dev       auto-restart the worker(s) on code changes
  #   --isolated  run one worker per queue via supervisord, so each queue gets
  #               its own concurrency and they can't block each other
  #
  # The celery queues (see `CELERY_TASK_ROUTES` in the django settings) can be
  # consumed in one of three topologies:
  #   1. `celery` (default): a single worker consumes all queues
  #      (`-Q celery,import,tika`), so tasks are never stranded but the queues
  #      share one concurrency pool and can block each other.
  #      This should be chosen for simple setups where no dossier import or even
  #      no alexandria is used.
  #   2. `celery --isolated`: one container in which supervisord runs one worker
  #      per queue (see `supervisord.ini`), giving independent concurrency
  #      without extra containers (see Kt. SG).
  #      This setup should be chosen as soon as dossier import or heavy
  #      alexandria (tika) usage is enabled, as those long-running tasks would
  #      block the other queues otherwise.
  #   3. Split containers: several `celery` containers, each pinned to one queue
  #      via the `CELERY_QUEUE` env var, giving every queue its own concurrency
  #      and independent scaling (see Kt. SO & Kt. GR).
  #      This setup should be chosen if you have the same requirements as 2. but
  #      you also want to limit resources (e.g. CPUs / MEM) **per queue**.
  dev="false"
  isolated="false"
  for arg in "$@"; do
    case "$arg" in
      --dev) dev="true" ;;
      --isolated) isolated="true" ;;
      *) ;;
    esac
  done

  wait-for-it "${REDIS_HOST:-redis}:${REDIS_PORT:-6379}"

  wrapper=""
  if [ "$dev" = "true" ]; then
    wrapper="watchmedo auto-restart -d . --recursive -p *.py --"
  fi

  if [ "$isolated" = "true" ]; then
    export CELERY_CONCURRENCY_DEFAULT_QUEUE="${CELERY_CONCURRENCY_DEFAULT_QUEUE:-2}"
    export CELERY_CONCURRENCY_IMPORT_QUEUE="${CELERY_CONCURRENCY_IMPORT_QUEUE:-1}"
    export CELERY_CONCURRENCY_TIKA_QUEUE="${CELERY_CONCURRENCY_TIKA_QUEUE:-1}"

    exec $wrapper supervisord -c /app/supervisord.ini
  fi

  # A single worker consuming all queues (or the queue named in CELERY_QUEUE).
  exec $wrapper celery -A camac worker -l INFO -E -O fair \
    -n "${CELERY_QUEUE:-celery}@%h" \
    -Q "${CELERY_QUEUE:-celery,import,tika}"
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
  echo "   - celery            to run the celery service, possible arguments:"
  echo "      --dev            to auto-restart the worker(s) on code changes"
  echo "      --isolated       to run one worker per queue (independent concurrency)"
  echo "   - celery-beat       to run the celery beat scheduler"
  echo "   - celery-beat-dev   to run the celery beat scheduler in development mode"
  echo "   - webdav            to run the webdav server via gunicorn and webdav.wsgi"
  echo "   - noop              Just start the container. Run no migrations, no server. Only for CI"
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
    run_gunicorn
    ;;
  gunicorn_k8s )
    # K8s mode: All setup (loadconfig, migrate) must be done explicitly
    # in an init task or similar
    run_gunicorn
    ;;
  celery )
    shift
    run_celery "$@"
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
  noop )
    echo "NOOP - Sleeping now"
    sleep inf
    ;;
  * )
    exec "$@"
    ;;
esac
