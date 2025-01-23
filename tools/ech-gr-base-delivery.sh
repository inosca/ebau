#!/bin/bash

declare -A credentials

credentials=(
	["gemeinde-chur"]="..."	
)

for i in "${!credentials[@]}"
do
	echo "----"
	echo "Logging in as: $i using secret ${credentials[$i]}"
	token=$(curl -s --request POST \
		--url 'https://test.ebau.gr.ch/auth/realms/ebau/protocol/openid-connect/token' \
		--header 'content-type: application/x-www-form-urlencoded' \
		--data grant_type=client_credentials \
		--data scope=openid \
		--data client_id=$i \
		--data client_secret=${credentials[$i]} | jq -r '.access_token')

	# curl -X GET "https://www.ebau.apps.be.ch/api/v1/me" -H "Authorization: Bearer $token"
	curl -X GET 'https://test.ebau.gr.ch/ech/v1/application/2360' \
  -H "Authorization: Bearer $token" \
  -H 'accept: application/xml' \
  -H 'x-camac-group: 20134' \
  -H 'Content-Type: application/xml'
done

