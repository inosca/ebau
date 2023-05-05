#!/bin/bash

# load .env file if it is present. We don't use 'xargs' because it isn't installed
# and installing packages is discouraged.
# https://www.keycloak.org/server/containers#_installing_additional_rpm_packages
# https://gist.github.com/mihow/9c7f559807069a03e302605691f85572?permalink_comment_id=4099982#gistcomment-4099982
if [ $ENV_FILE ]; then
    export $(grep -vE "^(#.*|\s*)$" $ENV_FILE)
fi

exec /opt/keycloak/bin/kc.sh $@
