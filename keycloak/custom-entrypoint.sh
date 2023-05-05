#!/bin/bash

if [ $ENV_FILE ]; then
    export $(grep -vE "^(#.*|\s*)$" $ENV_FILE)
fi

exec /opt/keycloak/bin/kc.sh $@
