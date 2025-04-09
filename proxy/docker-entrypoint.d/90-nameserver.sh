#!/bin/sh -

set -uf

CONFIG_IN=/etc/nginx/conf.d/default.conf.in
CONFIG_OUT=/etc/nginx/conf.d/default.conf

echo "Reading nameserver information from /etc/resolv.conf"
nameserver=
while read -r line; do
	case "$line" in (''|'#'*)
		continue  # empty or commented line, ignore
	esac
	# shellcheck disable=SC2086
	set -- $line
	[ $# -ge 2 ] || continue
	[ "$1" = nameserver ] || continue
	shift
	nameserver=$1
	break
done </etc/resolv.conf
if [ -z "$nameserver" ]; then
	echo 'Nameserver entry not found in /etc/resolv.conf' >&2
	exit 1
fi

echo "Setting nameserver to $nameserver"
if ! sed -re "s/^resolver\\s+\\S+(.*);.*\$/resolver $nameserver\\1;/" \
	<"$CONFIG_IN" >"$CONFIG_OUT"
then
	echo 'Could not replace resolver entry in nginx configuration' >&2
	exit 1
fi
