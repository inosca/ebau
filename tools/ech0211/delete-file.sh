#!/bin/bash
source ./config.sh

echo "---------------------------"
echo "eCH0211 - DELETE file"
echo "---------------------------"

file_uuid="f5db99e8-c4cc-4791-8cdf-055765df5cce"

for i in "${!ech0211_credentials[@]}"
do
	ech0211_login "$i" "${ech0211_credentials[$i]}"
	echo " > perform request[delete file] for client_id: $i"
	echo -e "\n---------------------------"
	curl -X DELETE "${ech0211_endpoint}/ech/v1/files/${file_uuid}" \
	-H "Authorization: Bearer $token" \
	-H 'accept: application/json' \
	-H "x-camac-group: ${camac_group_id}" \
	-H 'Content-Type: application/json'
	echo -e "\n---------------------------"
done
