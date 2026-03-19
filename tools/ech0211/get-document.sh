#!/bin/bash
source ./config.sh

echo "---------------------------"
echo "eCH0211 - GET documents"
echo "---------------------------"

document_id="4c094968-dddf-4534-b75c-2605261efe40"

for i in "${!ech0211_credentials[@]}"
do
	ech0211_login "$i" "${ech0211_credentials[$i]}"
	echo " > perform request[get documents] for client_id: $i"
	echo -e "\n---------------------------"
	curl -D - -X GET "${ech0211_endpoint}/ech/v1/documents/${document_id}" \
	-H "Authorization: Bearer $token" \
	-H 'accept: application/vnd.api+json' \
	-H "x-camac-group: ${camac_group_id}"
	echo -e "\n---------------------------"
done
