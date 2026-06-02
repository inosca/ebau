#!/bin/sh -

# Set/reset variables for using eBau with locally started Ember applications.
# Invoked by the `ember-dev` and `ember-dev-reset` Makefile targets in the
# project top-level.

dev_enable()
{
	if docker compose config | grep -q php; then
		sed -re 's|ember\.development.*|ember\.development = true|' -i "$APPLICATION_INI"
		sed -re 's|portal\.uri.*|portal\.uri = http://localhost:4200|' -i "$APPLICATION_INI"
		sed -re 's|baseURLPortal.*|baseURLPortal = http://localhost:4200|' -i "$APPLICATION_INI"
		echo "Set ember.development = true in application.ini"
		# shellcheck disable=SC2016
		sed -re 's|^(\s*proxy_pass\s+http://)ember-camac-ng(.+)|\1host.docker.internal:4300\2|g' -i "$PROXY_CONFIG"
		echo "Set base URL to 'host.docker.local:4300' in proxy config"
	else
		grep -q INTERNAL_URL .env || echo INTERNAL_URL=http://localhost:4400 >> .env
		echo "Added local INTERNAL_URL to .env."
	fi
	grep -q PORTAL_URL .env || echo PORTAL_URL=http://localhost:4200 >> .env
	echo "Added local PORTAL_URL to .env."
}

dev_reset()
{
	if docker compose config | grep -q php; then
		sed -re 's|ember\.development.*|ember.development = false|' -i "$APPLICATION_INI"
		case "$APPLICATION" in
			(kt_schwyz) portal_url=ebau-rest-portal ;;
			(*) portal_url=ebau-portal ;;
		esac
		sed -re "s|portal\\.uri.*|portal.uri = http://${portal_url}.localhost|" -i "$APPLICATION_INI"
		sed -re "s|baseURLPortal.*|baseURLPortal = http://${portal_url}.localhost|" -i "$APPLICATION_INI"
		echo "Set ember.development = false in application.ini"
		# shellcheck disable=SC2016
		sed -re 's|^(\s*proxy_pass\s+http://)host\.docker\.internal:4300(.+)|\1ember-camac-ng\2|g' -i "$PROXY_CONFIG"
		echo "Set base URL to 'ember-camac-ng' in proxy config"
	fi
	sed -i '/PORTAL_URL/d' .env
	sed -i '/INTERNAL_URL/d' .env
	echo "Removed PORTAL_URL and INTERNAL_URL from .env."
}

# shellcheck disable=SC1091
APPLICATION=$(export $(grep -Ev '^(UID=|\s*#|\s*$)' .env | xargs) && echo "$APPLICATION")
APPLICATION_INI=php/$APPLICATION/configs/application.ini
PROXY_CONFIG=proxy/$APPLICATION.conf
readonly APPLICATION APPLICATION_INI PROXY_CONFIG

dev_"$1"
