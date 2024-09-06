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

# Default command is "uwsgi". This implies production mode
# and we only load config in prod mode.
if [ "$#" -lt 1 ]; then
  echo "ERROR: NO COMMAND GIVEN: $@"
  echo "Need to pass either one of these:"
  echo "   - uwsgi      to run the production server (load config)"
  echo "   - qcluster   to run the django-q service"
  echo "   - devserver  to run the development server (takes additional args"
  echo  "    if needed)"
  echo ""
  echo "Any other command will be run as-is (for example you can run bash"
  echo "or any other mgmt command)"
  exit 1
fi

case "$1" in
  uwsgi )
    do_setup
    loadconfig
    exec "$1"
    ;;
  devserver )
    do_setup
    exec python manage.py runserver 0:80 --pythonpath /app/$APPLICATION
    ;;
  qcluster )
    do_setup no-migrate
    exec python manage.py qcluster --pythonpath /app/$APPLICATION
    ;;
  * )
    exec "$@"
    ;;
esac
