#!/bin/sh
set -e

if [ ! -d "/app/assets/node_modules" ]; then
    if [ ! -d "/opt/node_modules" ]; then
        echo "/opt/node_modules does not exist. Exiting."
        exit 1
    fi
    cp -r  /opt/node_modules/ /app/assets/node_modules/
fi

mix deps.get

mix phx.server
