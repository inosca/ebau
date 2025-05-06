#!/bin/bash
declare -A ech0211_credentials=(
	["gemeinde-chur"]="xxx"
	# ["gemeinde-davos"]="xxx"
)
keycloak_endpoint="http://ebau-keycloak.localhost"
ech0211_endpoint="http://ember-ebau.localhost"
camac_group_id="10035"

ech0211_login() {
	local client_id=$1
	local client_secret=$2

	echo " > logging in as: $client_id using secret ${client_secret}"
	token=$(curl -s --request POST \
		--url "${keycloak_endpoint}/auth/realms/ebau/protocol/openid-connect/token" \
		--header 'content-type: application/x-www-form-urlencoded' \
		--data grant_type=client_credentials \
		--data scope=openid \
		--data client_id=$client_id \
		--data client_secret=$client_secret | jq -r '.access_token')

	if [ -z "$token" ]; then
		echo " ### failed to retrieve token for client_id: $client_id"
		exit 1
	fi

	echo " > token retrieved successfully for client_id: $client_id"
}
