#!/bin/bash

declare -A credentials

credentials=(
	["gemeinde-foo"]="*********************"
	["gemeinde-bar"]="*********************"
)

for i in "${!credentials[@]}"
do
	echo "----"
	echo "Logging in as: $i using secret ${credentials[$i]}"
	token=$(curl -s --request POST \
		--url 'https://sso.be.ch/auth/realms/ebau/protocol/openid-connect/token' \
		--header 'content-type: application/x-www-form-urlencoded' \
		--data grant_type=client_credentials \
		--data client_id=$i \
		--data client_secret=${credentials[$i]} | jq -r '.access_token')

	curl -X GET "https://www.ebau.apps.be.ch/api/v1/me" -H "Authorization: Bearer $token"
done

