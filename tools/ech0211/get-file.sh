#!/bin/bash
source ./config.sh

echo "---------------------------"
echo "eCH0211 - GET file"
echo "---------------------------"

file_link="${ech0211_endpoint}/ech/v1/files/411d1971-e719-4fc8-860e-cacc52858dd9"
# file_link="${ech0211_endpoint}/api/v1/attachments/files/?attachments=23000007"

for i in "${!ech0211_credentials[@]}"
do
	ech0211_login "$i" "${ech0211_credentials[$i]}"
	echo " > perform request[get file] for client_id: $i"
	echo -e "\n---------------------------"
	curl -D - -X GET ${file_link} \
	-H "Authorization: Bearer $token" \
	-H 'accept: application/json' \
	-H "x-camac-group: ${camac_group_id}" \
	-H 'Content-Type: application/json'
	echo -e "\n---------------------------"
done
