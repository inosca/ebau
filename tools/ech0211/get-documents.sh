#!/bin/bash
source ./config.sh

echo "---------------------------"
echo "eCH0211 - GET documents"
echo "---------------------------"

dossier_id="12"

for i in "${!ech0211_credentials[@]}"
do
	ech0211_login "$i" "${ech0211_credentials[$i]}"
	echo " > perform request[get documents] for client_id: $i"
	echo -e "\n---------------------------"
	curl -D - -X GET "${ech0211_endpoint}/ech/v1/documents?instance=${dossier_id}&page%5Bnumber%5D=1&page%5Bsize%5D=10" \
	-H "Authorization: Bearer $token" \
	-H 'accept: application/vnd.api+json' \
	-H "x-camac-group: ${camac_group_id}"
	echo -e "\n---------------------------"
done
