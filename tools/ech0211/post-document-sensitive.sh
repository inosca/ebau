#!/bin/bash
source ./config.sh

echo "---------------------------"
echo "eCH0211 - POST document sensitive"
echo "---------------------------"

document_id="a4c3a63e-5020-4b6b-a4b0-9f518bf6864c"

for i in "${!ech0211_credentials[@]}"
do
	ech0211_login "$i" "${ech0211_credentials[$i]}"
	echo " > perform request[post document sensitive] for client_id: $i"
	echo -e "\n---------------------------"
	curl -X POST "${ech0211_endpoint}/ech/v1/documents/${document_id}/sensitive" \
	-H "Authorization: Bearer $token" \
	-H 'accept: application/vnd.api+json' \
	-H "x-camac-group: ${camac_group_id}"\
	-H 'Content-Type: application/json'
	echo -e "\n---------------------------"
done
