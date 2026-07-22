#!/bin/sh
set -euf

# We set all "needed" variables to some fake (but not problematic) value
# and run the commands to set the static data (translations, static files)
#
# This is fine for building static stuff. We just need to ensure all
# apps are loaded, but the only dynamic one is Silk
#
# Note: The APPLICATION value is set by the CI script (or .env), as it's
# needed to correctly collect some canton-specific static files

export VISIBILITY_CLASSES="caluma.caluma_core.visibilities.Any"
export PERMISSION_CLASSES="caluma.caluma_core.permissions.AllowAny"
export MANABI_SHARED_KEY="xyz"

export DJANGO_SECRET_KEY=none
export DJANGO_ALLOWED_HOSTS="*"
export DJANGO_PUBLIC_BASE_URL='localhost'
export DJANGO_INTERNAL_BASE_URL='localhost'
export DJANGO_MEDIA_ROOT=/app/media/

export DATABASE_PASSWORD=none
export DJANGO_DEFAULT_FROM_EMAIL=none@example.com
export DJANGO_SERVER_EMAIL=none@example.com
export DJANGO_EMAIL_HOST=localhost
export GWR_FERNET_KEY=none
export GWR_WSK_ID=9


./manage.py collectstatic --noinput
./manage.py compilemessages
